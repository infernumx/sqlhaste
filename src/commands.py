from typing import Any, Callable, TYPE_CHECKING
from types import UnionType
from dataclasses import dataclass
from .types import OptionalString
import traceback
import inspect

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


def consume_rest(fn: Callable, data: str) -> tuple[list[str], str, int]:
    """
    Function to handle command calls with 1 string, splitting by
    whitespace until the first positional argument is found.
    Returns a tuple of the arguments and the rest of the string, along
    with the index of the first positional-only argument.
    """
    args: list[str] = data.split()
    try:
        pos_idx: int = str(inspect.signature(fn)).split(",").index(" /")
        return args[:pos_idx], " ".join(args[pos_idx:]), pos_idx
    except ValueError:
        return args, "", -1


def call(user_input: str, terminal: "Terminal"):
    if not user_input:
        return

    name: str = user_input.split()[0]

    if cmd := _commands.get(name):
        consumed: tuple[list[str], str, int] = consume_rest(
            _commands[name].func, user_input
        )
        args: list[str] = consumed[0][1:]
        rest: str = consumed[1]
        pos_idx: int = consumed[2]
        n: int = cmd.func.__code__.co_argcount - 1
        annotations: list[Any] = list(cmd.func.__annotations__.values())
        if n != len(annotations):
            if pos_idx != -1:
                return cmd.func(terminal, *args[:n], rest)
            return cmd.func(terminal, *args[:n])
        if pos_idx != -1:
            annotations = annotations[: pos_idx - 1]  # account for 'self'
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

        if pos_idx != -1:
            return cmd.func(terminal, *args[:n], rest)
        return cmd.func(terminal, *args[:n])
    else:
        terminal.console.print(f"Command by the name of {name} not found.")


def get_commands():
    return list(_commands.values())


def get_command(cmd_name: str) -> Command | None:
    return _commands.get(cmd_name)
