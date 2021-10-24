from abc import ABC, abstractmethod
from src.terminal import Terminal
from src.types import SQLEngine, SQLResults, SQLResult


class EngineBase(ABC):
    def __init__(self, cls: SQLEngine, engine_type: str, db_name: str):
        self.engine_type: str = engine_type
        self.db_name: str = db_name
        self.terminal: Terminal = Terminal(cls)

    @abstractmethod
    def execute(
        self, query: str, *args, fetch_all: bool = True
    ) -> SQLResults | SQLResult:
        pass

    @abstractmethod
    def get_table_names(self) -> SQLResults:
        pass

    @abstractmethod
    def get_rows_by_table_name(self, table_name: str) -> SQLResults:
        pass
