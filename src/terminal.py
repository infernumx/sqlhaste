from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich import box
from typing import Any
from .types import SQLEngine, SQLResults, OptionalString
from .pagination import Paginator
import src.commands as commands
import shlex
from sqlite3 import OperationalError


class Terminal:
    _state: dict[str, Any] = {}

    def __init__(self, engine: SQLEngine):
        # Enforce borg pattern for references
        # pointing all states to the exact same console & engine

        if not Terminal._state:
            self.console: Console = Console()
            self.engine: SQLEngine = engine

            self.active_table: str = self.engine.get_table_names()[0]
            self.db_page: int = 1
            self.paginator: Paginator = Paginator([], 0)
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
        tables: list[str] = self.engine.get_table_names()

        # Table name -> row data
        panel_data: dict[str, SQLResults] = {
            name: self.engine.get_rows_by_table_name(name) for name in tables
        }

        # Maximum height to output based on Rich console height
        height: int = self.console.height - 2

        # Maximum rows to display for pagination
        max_page: int = height - 4

        self.paginator = Paginator(panel_data[self.active_table], max_page)

        page_count: int = max(1, self.paginator.get_page_count())

        # Table names with active table set
        table_names: list[str] = [""] * (height - 2)

        for i, name in enumerate(list(panel_data.keys())):
            if name != self.active_table:
                table_names[i] = name
            else:
                table_names[i] = f"[green underline]{name}[/green underline]"

        table_names[-1] = f"Page {self.db_page}/{page_count}".center(13)

        # Header column names for table data
        columns: list[tuple[str, str]] = [
            (col[1], col[2])
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
        for name, dtype in columns:
            sql_data.add_column(
                f"[#03fcec]{name}[/#03fcec] - [bold yellow]{dtype}[/bold yellow]",
                justify="center",
            )

        # Add SQL table data
        for row in self.paginator.get_page(self.db_page - 1):
            if row:
                sql_data.add_row(*map(str, row))

        self.console.print(layout, height=height)

    def halt(self) -> None:
        """Halts output until a key is pressed"""
        self.console.input("[underline]Press any key to continue.[/underline]")

    def error(self, msg: str) -> None:
        self.console.print(f"[red underline]Error: {msg}[/red underline]")
        self.halt()

    def success(self, msg: str) -> None:
        self.console.print(f"[green underline]{msg}[/green underline]")
        self.halt()

    def main_screen(self) -> None:
        self.console.rule("SQLHaste")
        self.show_db()
        response: str = self.console.input("[blue]$ [/blue]")
        commands.call(response, self)

    @commands.command(usage="help <command; optional>")
    def help(self, cmd_name: OptionalString = None) -> None:
        """Describes all commands available, or a specified command"""
        if isinstance(cmd_name, str):
            if command := commands.get_command(cmd_name):
                self.console.print(
                    f"- {command.name}: {command.usage}\n  {command.desc}"
                )
            else:
                self.error(f"Command {cmd_name!r} does not exist.")
        else:
            for cmd in commands.get_commands():
                self.console.print(f"- {cmd.name}: {cmd.usage}\n  {cmd.desc}")
        self.halt()

    @commands.command(name="exit")
    def _exit(self):
        """Exits the program"""
        exit()

    @commands.command(usage="swap <table_name>")
    def swap(self, table_name: str) -> None:
        """Swaps to a different table"""
        tables: list[str] = self.engine.get_table_names()
        if table_name not in tables:
            self.error(f"Table {table_name} does not exist")
            return
        self.active_table = table_name
        self.db_page = 1
        self.success(f"Table swapped to [underline]{table_name}[/underline]!")

    @commands.command(name="page", usage="page <page_number>")
    def set_page(self, page: int):
        """Sets the page for the active table"""
        if page < 1 or page > self.paginator.get_page_count():
            self.error("Page number out of range")
            return
        self.db_page = page
        self.success(f"Page switched to {page}")

    @commands.command(usage="insert <values>")
    def insert(self, /, values: str):
        """Inserts a new row into the active table"""
        self.engine.insert(self.active_table, shlex.split(values))
        self.success(f"Inserted {values!r} into {self.active_table}")

    @commands.command(usage="delete <where> <value>")
    def delete(self, where: str, value: str):
        """Deletes a row from the active table"""
        self.engine.delete(self.active_table, where, value)
        self.success(f"Deleted {value!r} from {self.active_table}")

    @commands.command(usage="update <where> <value> <new_value>")
    def update(self, where: str, value: str, new_value: str):
        """Updates a row in the active table"""
        self.engine.update(self.active_table, where, value, new_value)
        self.success(f"Updated {value!r} to {new_value!r} in {self.active_table}")

    # this command executes a query and displays the results
    @commands.command(usage="query <query>")
    def query(self, /, query: str):
        """Executes a query and displays the results"""
        try:
            print(self.engine.execute(query))
            self.halt()
        except OperationalError as e:
            self.error(f"{e}")
