from .engines.sqlite import SQLiteManager
from .types import SQLEngine, SQLResults, SQLResult


class DatabaseManager:
    def __init__(self, db_name: str, engine_type: SQLEngine):
        match engine_type:
            case "SQLite3":
                self.sql_engine: SQLEngine = SQLiteManager(db_name)
            case "MySQL":
                pass
            case "Postgres":
                pass

    def display(self) -> None:
        self.sql_engine.terminal.main_screen()

    def execute(self, query: str, *args, fetch_all=True) -> SQLResults | SQLResult:
        return self.sql_engine.execute(query, *args, fetch_all=fetch_all)