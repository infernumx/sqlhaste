from typing import Any, Callable
from dataclasses import dataclass

_commands: dict[str, Any] = {}


@dataclass
class Command:
    func: Callable
    name: str
    desc: str


def command(name=None):
    def inner(fn):
        nonlocal name
        name = name or fn.__name__
        _commands[name] = Command(fn, name, fn.__doc__ or "No Description")
        return fn

    return inner


def call(name, *args, **kwargs):
    if cmd := _commands.get(name):
        return cmd.func(*args, **kwargs)


def get_commands():
    return list(_commands.values())
