import logging
import sys
from scattack.gui.command import CommandQueue, ResultQueue
from scattack.gui.executor import CommandExecutor
from .app import App


def main():
    command_queue = CommandQueue()
    result_queue = ResultQueue()

    root = logging.getLogger()
    app = App(logger=root, cmd_queue=command_queue, result_queue=result_queue)
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    executor = CommandExecutor(command_queue, result_queue)
    executor.start()
    app.run()
    executor.stop()


exit(main())
