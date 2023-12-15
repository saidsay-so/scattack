import logging
import sys
from scattack.gui.executor import CommandExecutor
from scattack.gui.command import queues
from .app import App


def main():
    app = App()
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)
    executor = CommandExecutor(queues.command_queue, queues.result_queue)
    executor.start()
    app.run()


exit(main())
