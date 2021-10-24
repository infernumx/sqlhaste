from typing import Any, Callable, Union, Optional, TYPE_CHECKING
from types import UnionType, NoneType
from dataclasses import dataclass
from .types import OptionalString
import traceback

if TYPE_CHECKING:
    from src.terminal import Terminal

_commands: dict[str, Any] = {}


@dataclass
class Command:
    func: Callable
    name: str
    desc: str
    usage: str


def command(name: OptionalString = None, usage: OptionalString = ""):
    def inner(fn):
        nonlocal name
        name = name or fn.__name__
        doc = fn.__doc__ or "No Description"
        _commands[name] = Command(fn, name, doc, usage)
        return fn

    return inner


def call(user_input: str, terminal: "Terminal"):
    if not user_input:
        return

    parsed: list[Any] = user_input.split()
    name: str = parsed[0]
    args: list[Any] = parsed[1:]

    if cmd := _commands.get(name):
        n: int = cmd.func.__code__.co_argcount - 1
        annotations: list[Any] = list(cmd.func.__annotations__.values())
        if n != len(annotations):
            return cmd.func(terminal, *args[:n])

        try:
            # Attempt type conversion based on function annotations
            for i, annotation_type in enumerate(annotations):
                # Argument has a single annotation, use it to convert
                if not isinstance(annotation_type, UnionType):
                    args[i] = annotation_type(args[i])
                    continue

                # Attempt conversion using type union list
                for conv_type in annotation_type.__args__:
                    if conv_type == type(None):
                        continue

                    # Use the first result that produces a truthy value
                    if res := conv_type(args[i]):
                        args[i] = res
                        break
        except Exception as e:
            traceback.print_exc()
            return

        return cmd.func(terminal, *args[:n])
    else:
        terminal.console.print(f"Command by the name of {name} not found.")


def get_commands():
    return list(_commands.values())


def get_command(cmd_name: str) -> Command | None:
    return _commands.get(cmd_name)
