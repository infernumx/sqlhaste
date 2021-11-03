#!/usr/bin/env python3

from src import DatabaseManager
from rich.console import Console
import sys
import glob


def get_db_files() -> list[str]:
    return glob.glob("*.db")


def main() -> None:
    if len(sys.argv) < 3:
        # Ask for database name and engine since they were not passed as arguments
        console: Console = Console()
        console.rule("SQLHaste")
        # print all available databases
        console.print("[underline]Available databases:[/underline]")
        for db in get_db_files():
            console.print(f"[yellow]{db}[/yellow]")
        db_name: str = console.input(
            ">> Input database name to open, or type a new database name to create one: "
        )
        db_engine: str = console.input(
            ">> Input database engine to use (SQLite, MySQL, PostgreSQL): "
        )
    else:
        db_name, db_engine = sys.argv[1], sys.argv[2]
    mgr: DatabaseManager = DatabaseManager(db_name, db_engine)
    mgr.display()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
