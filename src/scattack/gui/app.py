from logging import Logger
from scattack.gui.alert import AlertWindow
from scattack.gui.tabs.arp_poison.layout import ArpPoisonFrame
from scattack.gui.command import (
    CommandCompleted,
    CommandEvent,
    CommandQueue,
    CommandStartRequest,
    CommandStopRequest,
    ResultQueue,
    StartCommand,
    StopCommand,
    TabCommandQueue,
)
from scattack.gui.dhcp_starve.layout import DhcpStarveFrame
from scattack.gui.executor import AbortedCommandExecution
from scattack.gui.tabs.wifi_deauth.layout import WifiDeauthFrame

from tkinter import ttk
import tkinter


class TabView(ttk.Notebook):
    def __init__(self, *args, queue: TabCommandQueue, **kwargs):
        super().__init__(*args, **kwargs)

        deauth = self.add(WifiDeauthFrame(queue=queue), text="Wi-Fi Deauthentification")

        arp = self.add(ArpPoisonFrame(queue=queue), text="ARP Cache Poisoning")

        dhcp = self.add(DhcpStarveFrame(queue=queue), text="DHCP Starvation")


class App(tkinter.Tk):
    def __init__(
        self,
        *args,
        logger: Logger,
        result_queue: ResultQueue,
        cmd_queue: CommandQueue,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.logger = logger

        self.result_queue = result_queue
        self.cmd_queue = cmd_queue
        self.tab_cmd_queue = TabCommandQueue()
        self.callbacks = {}

        self.alert_window = None

        self.title("SCAttack")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.geometry("800x600")
        self.minsize(500, 400)
        self.tab_view = TabView(self, queue=self.tab_cmd_queue)
        self.tab_view.pack(fill="both", expand=True)

        self.after(100, self.result_listener)
        self.after(100, self.command_req_listener)

    def command_req_listener(self):
        while not self.tab_cmd_queue.empty():
            try:
                req = self.tab_cmd_queue.get_nowait()
            except:
                break

            self.logger.debug(
                "A new command request has been popped: %s (%r)",
                req.command_id,
                type(req).__name__,
            )

            match req:
                case CommandStartRequest(
                    callback, fun, args, kwargs, still_valid, command_id
                ):
                    self.logger.debug("Starting command %s", command_id)
                    self.callbacks[command_id] = callback
                    self.cmd_queue.put(
                        StartCommand(command_id, fun, args, kwargs, still_valid)
                    )
                case CommandStopRequest(command_id):
                    self.logger.debug("Stopping command %s", command_id)
                    self.cmd_queue.put(StopCommand(command_id))

            self.tab_cmd_queue.task_done()
        # Reschedule the listener
        self.after(100, self.command_req_listener)

    def result_listener(self):
        """Listen for results from the command executor"""
        while not self.result_queue.empty():
            try:
                result = self.result_queue.get_nowait()
            except:
                break

            self.logger.debug(
                "A new result has been popped: %s",
                result.command_id,
            )
            self.on_result(result)
            self.result_queue.task_done()
        # Reschedule the listener
        self.after(100, self.result_listener)

    def on_result(self, event: CommandEvent):
        """Handle a result from the command executor"""
        self.logger.debug("Handling result %s", event)
        self.logger.debug("Callbacks: %s", repr(self.callbacks))

        self.callbacks[event.command_id](event)

        match event:
            case CommandCompleted(id, result):
                self.logger.debug("Command %s completed with result %s", id, result)
                self.callbacks.pop(event.command_id)

                match result:
                    case None | AbortedCommandExecution():
                        pass
                    case Exception() as e:
                        self.show_error(e)

    def show_error(self, e: Exception):
        self.toplevel_window = AlertWindow(self, message=str(e))

    def quit(self, event=None):
        self.destroy()

    def run(self):
        self.mainloop()
