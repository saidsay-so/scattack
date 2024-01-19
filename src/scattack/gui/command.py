from queue import Queue
from dataclasses import dataclass, field
from typing import Callable, Any
from collections.abc import Iterable
from uuid import uuid4

CommandId = str


@dataclass
class StartCommand:
    id: CommandId
    """The unique id of the command"""
    fun: Callable[..., Any]
    """The function to execute"""
    args: Iterable
    """The arguments to pass to the function"""
    kwargs: dict[str, Any]
    """The keyword arguments to pass to the function"""
    condition: Callable[[], bool]
    """The condition to check if the command should still be executed"""


@dataclass
class StopCommand:
    id: CommandId


Command = StartCommand | StopCommand


@dataclass
class CommandEventBase:
    command_id: CommandId
    """The id of the command"""


@dataclass
class CommandCompleted(CommandEventBase):
    result: Exception | None


@dataclass
class CommandScheduled(CommandEventBase):
    pass


CommandEvent = CommandCompleted | CommandScheduled


ResultQueue = Queue[CommandEvent]
CommandQueue = Queue[Command]


@dataclass
class CommandStartRequest:
    callback: Callable[[CommandEvent], None]
    # All fields of StartCommand except id
    fun: Callable[..., Any]
    args: Iterable
    kwargs: dict[str, Any]
    condition: Callable[[], bool]
    command_id: CommandId = field(default_factory=lambda: str(uuid4()))


@dataclass
class CommandStopRequest:
    command_id: CommandId


CommandRequest = CommandStartRequest | CommandStopRequest

TabCommandQueue = Queue[CommandRequest]
