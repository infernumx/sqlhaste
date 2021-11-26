from abc import ABC, abstractmethod
from typing import Any
from src.terminal import Terminal
from src.types import SQLEngine, SQLResults, SQLResult


class EngineBase(ABC):
    def __init__(self, cls: SQLEngine, engine_type: str, db_name: str):
        self.engine_type: str = engine_type
        self.db_name: str = db_name
        self.terminal: Terminal = Terminal(cls)

    @abstractmethod
    def execute_get_one(self, query: str, *args) -> SQLResult:
        pass

    @abstractmethod
    def execute_get_all(self, query: str, *args) -> SQLResults:
        pass

    @abstractmethod
    def get_table_names(self) -> list[str]:
        pass

    @abstractmethod
    def get_rows_by_table_name(self, table_name: str) -> SQLResults:
        pass

    @abstractmethod
    def get_table_info(self, table_name: str) -> SQLResults:
        pass

    @abstractmethod
    def insert(self, table_name: str, values: list[Any]) -> None:
        pass

    @abstractmethod
    def delete(self, table_name: str, where: str, value: Any) -> None:
        pass

    @abstractmethod
    def update(self, table_name: str, where: str, value: Any, new_value: Any) -> None:
        pass

    @abstractmethod
    def create_table(self, table_name: str, columns: list[str]) -> None:
        pass
