from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich import box
from typing import Any
from .types import SQLEngine, SQLResults
from .pagination import Paginator


class Terminal:
    _state: dict[str, Any] = {}

    def __init__(self, engine: SQLEngine):
        # Enforce borg pattern for references
        # pointing all states to the exact same console & engine

        if not Terminal._state:
            self.console: Console = Console()
            self.engine: SQLEngine = engine
            self.active_table = "dummy"
            Terminal._state = self.__dict__
        else:
            self.__dict__ = Terminal._state

    def collect_input(self) -> Any:
        input_options = [
            ("Change Table", self.change_table),
        ]

        while True:
            # Continuous input until valid number is received

            for index, option in enumerate(input_options, start=1):
                self.console.print(f"[red][{index}] {option[0]}", end="; ")
            response: str = self.console.input("[green]>> ")
            size: int = len(input_options)

            if response.isdigit() and 1 <= int(response) < size + 1:
                response = int(response)
                break

            self.console.print(
                f"[red underline]Please select a valid option (1-{size})."
            )

        opt, fn = input_options[response - 1]
        return fn()

    def create_dummy_db(self) -> None:
        pass

    def change_table(self) -> None:
        """Displays all contents of a specified table"""
        # TODO: allow viewing table scheme

        tables: SQLResults = [table[0] for table in self.engine.get_table_names()]
        while True:
            table_name: str = self.console.input("[green]>> New active table name: ")
            if table_name in tables:
                break
            self.console.print(f"[red]! Table {table_name!r} does not exist. ![/red]")
        self.active_table = table_name

    def edit_table(self) -> None:
        # TODO: allow altering table scheme
        pass

    def view_table_structure(self) -> None:
        pass

    def edit_table_structure(self) -> None:
        pass

    def execute_sql(self) -> None:
        pass

    def main_screen(self) -> None:
        # TODO: Pagination
        tables: SQLResults = self.engine.get_table_names()
        panel_data: dict[str, SQLResults] = {
            table[0]: self.engine.get_rows_by_table_name(table[0]) for table in tables
        }
        height: int = min(
            self.console.height - 2, len(panel_data[self.active_table]) + 4
        )
        max_page: int = height - 4
        table_names: list[str] = [
            name
            if name != self.active_table
            else f"[green underline]{name}[/green underline]"
            for name in list(panel_data.keys())
        ]
        column_names: list[str] = [
            col[1]
            for col in self.engine.execute(f"PRAGMA table_info({self.active_table})")
        ]
        sql_tables: Panel = Panel(
            "\n".join(table_names),
            expand=True,
            height=min(len(table_names) + 2, self.console.height),
            title=self.engine.db_name,
        )
        sql_data: Table = Table(expand=True, box=box.DOUBLE)
        layout: Layout = Layout()
        layout.split_row(
            Layout(sql_tables, name="left", size=20),
            Layout(sql_data, name="right"),
        )

        # Add SQL table columns
        for name in column_names:
            sql_data.add_column(name.title(), justify="center")

        # Add SQL table data
        for row in panel_data[self.active_table][:max_page]:
            sql_data.add_row(*map(str, row))

        self.console.print(layout, height=height)

        response: int = self.collect_input()
