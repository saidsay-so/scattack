import logging
import sys
from scattack.gui.command import CommandQueue, ResultQueue
from scattack.gui.executor import CommandExecutor
from .app import App

import sv_ttk


def main():
    command_queue = CommandQueue()
    result_queue = ResultQueue()

    root_logger = logging.getLogger()
    app = App(
        logger=root_logger.getChild("gui"),
        cmd_queue=command_queue,
        result_queue=result_queue,
    )
    root_logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    executor = CommandExecutor(
        command_queue, result_queue, root_logger.getChild("executor")
    )
    executor.start()

    sv_ttk.use_dark_theme()
    app.run()

    executor.stop()


exit(main())
