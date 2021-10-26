from .engines.sqlite import SQLiteManager
from .types import SQLEngine, SQLResults, SQLResult


class DatabaseManager:
    def __init__(self, db_name: str, engine_type: SQLEngine):
        if engine_type == "SQLite3":
            self.sql_engine: SQLEngine = SQLiteManager(db_name)
        elif engine_type == "MySQL":
            pass
        elif engine_type == "PostgreSQL":
            pass

    def display(self) -> None:
        while True:
            self.sql_engine.terminal.main_screen()

    def execute(self, query: str, *args, fetch_all=True) -> SQLResults | SQLResult:
        return self.sql_engine.execute(query, *args, fetch_all=fetch_all)
