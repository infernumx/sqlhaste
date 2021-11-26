from .engines import SQLiteManager, MySQLManager
from .types import SQLEngine, SQLResults, SQLResult


class DatabaseManager:
    def __init__(self, db_name: str, engine_type: str):
        self.sql_engine: SQLEngine
        if engine_type in ("sqlite3", "sqlite"):
            self.sql_engine = SQLiteManager(db_name)
        elif engine_type == "mysql":
            self.sql_engine = MySQLManager(db_name)
        elif engine_type == "postgresql":
            raise NotImplementedError("PostgreSQL is not supported yet.")

    def display(self) -> None:
        while True:
            self.sql_engine.terminal.main_screen()
