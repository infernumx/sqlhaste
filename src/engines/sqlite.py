from .base import EngineBase
from src.types import SQLResults, SQLResult
import sqlite3
from sqlite3 import Connection, Cursor


class SQLiteManager(EngineBase):
    def __init__(self, db_name: str):
        super().__init__(self, "SQLite", db_name)
        self.connection: Connection = sqlite3.connect(db_name)

    def execute(self, query: str, *args, fetch_all=True) -> SQLResults | SQLResult:
        with self.connection as cursor:
            result: Cursor = cursor.execute(query, args)
            if fetch_all:
                return result.fetchall()
            return result.fetchone()

    def get_table_names(self) -> SQLResults:
        return self.execute("SELECT name FROM sqlite_master WHERE type='table'")

    def get_rows_by_table_name(self, table_name: str) -> SQLResults:
        return self.execute(f"SELECT * FROM {table_name}")
