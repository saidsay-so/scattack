from logging import error, info
from threading import Thread

from .command import (
    CommandCompleted,
    CommandQueue,
    CommandScheduled,
    ResultQueue,
    StartCommand,
    StopCommand,
)


class AbortedCommandExecution(Exception):
    """An exception raised when a command execution is aborted"""

    pass


class CommandExecutor(Thread):
    """A thread that executes commands"""

    cmd_queue: CommandQueue
    """The queue of commands to execute"""

    def __init__(self, cmd_queue: CommandQueue, res_queue: ResultQueue):
        super().__init__()
        self.cmd_queue = cmd_queue
        self.res_queue = res_queue

    def run(self):
        """Execute the commands in the queue"""

        while True:
            command = self.cmd_queue.get()
            info(f"Executing command {command}")

            match command:
                case StartCommand(id, fun, args, kwargs, still_valid):
                    self.res_queue.put(CommandScheduled(id))
                    result = None
                    try:
                        while self.cmd_queue.empty() and still_valid():
                            fun(*args, **kwargs)
                        if not self.cmd_queue.empty():
                            result = AbortedCommandExecution(id)
                    except Exception as e:
                        result = e
                        error(f"Error executing command {command}: {result}")
                    finally:
                        self.res_queue.put(CommandCompleted(id, result))

                case StopCommand():
                    pass

            self.cmd_queue.task_done()
