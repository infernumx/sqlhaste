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

### Unix-based
- `./sqlhaste.py <db name> <engine>`
- `python3 sqlhaste.py <db name> <engine>`

### Windows
- `python sqlhaste.py <db name> <engine>`

Invoking the program without a database name and engine will prompt you for both inside the program instead, they are not required to be passed through the shell.
