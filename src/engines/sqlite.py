from .base import EngineBase
from src.types import SQLResults, SQLResult
from typing import Any, Literal, overload
import sqlite3
from sqlite3 import Connection, Cursor


class SQLiteManager(EngineBase):
    def __init__(self, db_name: str):
        self.connection: Connection = sqlite3.connect(db_name)
        super().__init__(self, "SQLite", db_name)

    @overload
    def execute(self, query: str, *args, fetch_all: Literal[True] = True) -> SQLResults:
        ...

    @overload
    def execute(self, query: str, *args, fetch_all: Literal[False]) -> SQLResult:
        ...

    def execute(
        self, query: str, *args, fetch_all: bool = True
    ) -> SQLResults | SQLResult:
        with self.connection as cursor:
            result: Cursor = cursor.execute(query, args)
            if fetch_all:
                return result.fetchall()
            return result.fetchone()

    def get_table_names(self) -> list[str]:
        return [
            row[0]
            for row in self.execute("SELECT name FROM sqlite_master WHERE type='table'")
            if row[0] != "sqlite_sequence"
        ]

    def get_rows_by_table_name(self, table_name: str) -> SQLResults:
        return self.execute(f"SELECT * FROM {table_name}")

    def coerce_datatypes(self, data: list[str]) -> list[Any]:
        """
        Attempts to convert passed arguments to proper datatypes
        in order to run the query.
        """
        coerced: list[Any] = []
        for item in data:
            if item == "NULL":
                coerced.append(None)
            elif item.isdigit():
                coerced.append(int(item))
            elif item.replace(".", "", 1).isdigit():
                coerced.append(float(item))
            else:
                coerced.append(item)
        return coerced

    def insert(self, table_name: str, values: list[str]) -> None:
        placeholders: str = ",".join(["?"] * len(values))
        values = self.coerce_datatypes(values)
        self.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", *values)

    def delete(self, table_name: str, where: str, value: Any) -> None:
        values = self.coerce_datatypes([value])
        self.execute(f"DELETE FROM {table_name} WHERE {where}=?", *values)

    def update(self, table_name: str, where: str, value: Any, new_value: Any) -> None:
        values = self.coerce_datatypes([new_value, value])
        print(f"UPDATE {table_name} SET {where}=? WHERE {where}=?", values)
        self.execute(f"UPDATE {table_name} SET {where}=? WHERE {where}=?", *values)
