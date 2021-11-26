from .base import EngineBase
from pymysql import connect, Connection
from pymysql.cursors import Cursor
from typing import Any
from src.types import SQLEngine, SQLResults, SQLResult


class MySQLManager(EngineBase):
    def __init__(self, db_name: str):
        self.connection: Connection = connect(
            host="127.0.0.1",
            user="user",
            password="user",
            cursorclass=Cursor,
            autocommit=True,
            database=db_name,
        )
        super().__init__(self, "MySQL", db_name)

    def execute_get_one(self, query: str, *args) -> SQLResult:
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            if data := cursor.fetchone():
                return data
        return ()

    def execute_get_all(self, query: str, *args) -> SQLResults:
        with self.connection.cursor() as cursor:
            cursor.execute(query, args)
            if data := cursor.fetchall():
                return list(data)
        return [()]

    def get_table_names(self) -> list[str]:
        return [table[0] for table in self.execute_get_all("SHOW TABLES")]

    def get_rows_by_table_name(self, table_name: str) -> SQLResults:
        return self.execute_get_all(f"SELECT * FROM {table_name}")

    def get_table_info(self, table_name: str) -> SQLResults:
        return [
            (result[2], result[0], result[1])
            for result in self.execute_get_all(f"DESCRIBE {table_name}")
        ]

    def insert(self, table_name: str, values: list[Any]) -> None:
        pass

    def delete(self, table_name: str, where: str, value: Any) -> None:
        pass

    def update(self, table_name: str, where: str, value: Any, new_value: Any) -> None:
        pass

    def create_table(self, table_name: str, columns: list[str]) -> None:
        self.execute_get_one(f"CREATE TABLE {table_name} ({', '.join(columns)})")
        self.connection.select_db(self.db_name)
