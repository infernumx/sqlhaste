# SQLHaste
SQLHaste features a shell-like approach to manage databases. To get started, simply type the command `help` in the terminal provided during execution.

## Requirements
- Python 3.10

## Installation

### Unix-based

- `python3 -m pip install -r requirements.txt`

### Windows

- `python -m pip install -r requirements.txt`

## Usage
SQLHaste can either be invoked by directly passing in a database name & engine, or by itself. If invoked by itself, it will ask you to select from any existing databases found in the root directory, or create a new database.

### Unix-based
- `./sqlhaste.py <db name> <engine>`
- `python3 sqlhaste.py <db name> <engine>`

### Windows
- `python sqlhaste.py <db name> <engine>`
