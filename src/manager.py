from .engines import SQLiteManager
from .types import SQLEngine, SQLResults, SQLResult


class DatabaseManager:
    def __init__(self, db_name: str, engine_type: str):
        self.sql_engine: SQLEngine
        if engine_type in ("sqlite3", "sqlite"):
            self.sql_engine = SQLiteManager(db_name)
        elif engine_type == "mysql":
            raise NotImplementedError("MySQL is not yet supported")
        elif engine_type == "postgresql":
            raise NotImplementedError("PostgreSQL is not supported yet.")

    def display(self) -> None:
        while True:
            self.sql_engine.terminal.main_screen()

    def execute(self, query: str, *args, fetch_all=True) -> SQLResults | SQLResult:
        return self.sql_engine.execute(query, *args, fetch_all=fetch_all)
