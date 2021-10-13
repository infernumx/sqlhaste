from rich.console import Console
from typing import Any
from .types import SQLEngine, SQLResults


class Terminal:
    _state: dict[str, Any] = {}

    def __init__(self, engine: SQLEngine):
        self.__dict__ = Terminal._state

        # Enforce borg pattern for references
        # pointing all states to the exact same console & engine
        if not Terminal._state.get("__borg__"):
            Terminal._state["__borg__"] = True
            self.console: Console = Console()
            self.engine: SQLEngine = engine

    def main_screen(self) -> None:
        tables: SQLResults = self.engine.get_table_names()

        self.console.print(f"[red underline]SQLite3 Tables for {self.engine.db_name}")

        for table_name in tables:
            rows: SQLResults = self.engine.get_rows_by_table_name(table_name[0])
            self.console.print(f"[green underline]{table_name[0]}")
            for i, data in enumerate(rows, start=1):
                self.console.print(f"[#f542ef]Row #{i}:[/#f542ef] {data}")
