from logging import Logger, getLogger
from threading import Thread

from .command import (
    CommandCompleted,
    CommandQueue,
    CommandScheduled,
    ResultQueue,
    StartCommand,
    StopCommand,
    StopExecutor,
)


class AbortedCommandExecution(Exception):
    """An exception raised when a command execution is aborted"""

    pass


class CommandExecutor(Thread):
    """A thread that executes commands"""

    cmd_queue: CommandQueue
    """The queue of commands to execute"""

    def __init__(
        self,
        cmd_queue: CommandQueue,
        res_queue: ResultQueue,
        logger: Logger = getLogger("CommandExecutor"),
    ):
        super().__init__()
        self.cmd_queue = cmd_queue
        self.res_queue = res_queue
        self.logger = logger

    def stop(self):
        """Stop the executor"""
        self.cmd_queue.put(StopExecutor())

    def run(self):
        """Execute the commands in the queue"""

        while True:
            command = self.cmd_queue.get()
            self.logger.info(f"Executing command {command}")

            match command:
                case StartCommand(id, fun, args, kwargs, still_valid):
                    self.res_queue.put(CommandScheduled(id))
                    result = None
                    try:
                        while self.cmd_queue.empty() and still_valid():
                            self.logger.debug(
                                (
                                    f"Executing command {command} ({id})"
                                    f"with args {args} and kwargs {kwargs}"
                                )
                            )
                            fun(*args, **kwargs)
                        if not self.cmd_queue.empty():
                            result = AbortedCommandExecution(id)
                            self.logger.info(f"Command {command} ({id}) aborted")
                    except Exception as e:
                        result = e
                        self.logger.error(
                            f"Error executing command {command}: {result}"
                        )
                    finally:
                        self.res_queue.put(CommandCompleted(id, result))
                        self.logger.info(f"Command {command} ({id}) completed")

                case StopCommand(id):
                    self.logger.debug(f"Command {command} ({id}) stopped")

                case StopExecutor():
                    self.logger.info("Stopping executor")
                    return

            self.cmd_queue.task_done()
