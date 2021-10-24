from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich import box
from typing import Any
from .types import SQLEngine, SQLResults
from .pagination import Paginator
import src.commands as commands


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

    def change_table(self) -> None:
        """Displays all contents of a specified table"""
        # TODO: allow viewing table scheme

        tables: list[str] = self.engine.get_table_names()
        while True:
            table_name: str = self.console.input("[green]>> New active table name: ")
            if table_name in tables:
                break
            self.console.print(f"[red]! Table {table_name!r} does not exist. ![/red]")
        self.active_table = table_name

    def show_db(self) -> None:
        # TODO: Pagination
        tables: list[str] = self.engine.get_table_names()

        # Table name -> row data
        panel_data: dict[str, SQLResults] = {
            name: self.engine.get_rows_by_table_name(name) for name in tables
        }

        # Maximum height to output based on Rich console height
        height: int = min(
            self.console.height - 2, len(panel_data[self.active_table]) + 4
        )

        # Maximum rows to display for pagination
        max_page: int = height - 4

        # Table names with active table set
        table_names: list[str] = [""] * (height - 2)

        for i, name in enumerate(list(panel_data.keys())):
            if name != self.active_table:
                table_names[i] = name
            else:
                table_names[i] = f"[green underline]{name}[/green underline]"

        table_names[-1] = "Page #1".center(15)

        # Header column names for table data
        column_names: list[str] = [
            col[1]
            for col in self.engine.execute(f"PRAGMA table_info({self.active_table})")
        ]

        # Table name panel (left side)
        sql_tables: Panel = Panel(
            "\n".join(table_names),
            expand=True,
            height=height,
            title=self.engine.db_name,
        )

        # SQL data table
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

    def main_screen(self) -> None:
        self.show_db()
        response: str = self.console.input("[blue]$ [/blue]")
        commands.call(response, self)
        self.console.input()

    @commands.command()
    def help(self) -> None:
        for command in commands.get_commands():
            self.console.print(f"- {command.name}: {command.desc}")
