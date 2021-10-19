#!/usr/bin/env python3

from src import DatabaseManager


def main() -> None:
    mgr: DatabaseManager = DatabaseManager("sample.db", "SQLite3")
    mgr.display()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
