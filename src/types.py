from typing import Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from src import SQLiteManager, MySQLManager, PostgresManager

SQLEngine = Union["SQLiteManager", "MySQLManager", "PostgresManager"]
SQLResult = tuple
SQLResults = list[SQLResult]
OptionalString = str | None
