#!/usr/bin/env python3

from src import DatabaseManager
from rich.console import Console
import sys


def main() -> None:
    if len(sys.argv) < 3:
        console: Console = Console()
        console.rule("SQLHaste")
        db_name: str = console.input(">> Input database name to open: ")
        db_engine: str = console.input(
            ">> Input database engine to use (SQLite, MySQL, PostgreSQL): "
        )
    else:
        db_name, db_engine = sys.argv[1:3]
    mgr: DatabaseManager = DatabaseManager(db_name, db_engine)
    mgr.display()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
