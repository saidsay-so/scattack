from queue import Queue
from dataclasses import dataclass
from typing import Callable, Any
from collections.abc import Iterable

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
    pass


Command = StartCommand | StopCommand


@dataclass
class CommandResult:
    result: Exception | None
    """The result of the command"""
    command_id: CommandId
    """The id of the command"""


ResultQueue = Queue[CommandResult]
CommandQueue = Queue[Command]


class _SingletonQueues:
    """A class that holds the queues for commands and results as
    a singleton"""

    command_queue: CommandQueue
    """The queue of commands to execute"""
    result_queue: ResultQueue
    """The queue of results from the commands"""

    def __init__(self):
        self.command_queue = CommandQueue()
        self.result_queue = ResultQueue()

    def _get_command_queue(self) -> Queue:
        """Get the queue of commands to execute"""
        return self.command_queue

    def _get_result_queue(self) -> Queue:
        """Get the queue of results from the commands"""
        return self.result_queue


queues = _SingletonQueues()


def submit_command(command: Command):
    """Submit a command to be executed"""
    queues._get_command_queue().put(command)
