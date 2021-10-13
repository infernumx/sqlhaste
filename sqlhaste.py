#!/usr/bin/env python3

from src import DatabaseManager
import sys


def main(option: str) -> None:
    mgr: DatabaseManager = DatabaseManager("sample.db", "SQLite3")
    if option == "display":
        mgr.display()
    elif option == "dummy":
        mgr.execute("DROP TABLE IF EXISTS dummy")
        mgr.execute("CREATE TABLE dummy (id INT, desc TEXT)")
        mgr.execute("INSERT INTO dummy VALUES (?, ?)", 1, "dummy value")


if __name__ == "__main__":
    main(sys.argv[1])
