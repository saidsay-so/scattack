from email.policy import default
from enum import StrEnum
import customtkinter
from scattack.gui.command import CommandId, CommandResult, queues
from scattack.gui.wifi_deauth.layout import WifiDeauthFrame


class CommandVirtualEventType(StrEnum):
    COMPLETED = "completed"


def id_virtual_event(id: CommandId, ev_type: CommandVirtualEventType):
    return f"<<{id}-{str(ev_type)}>>"


class TabView(customtkinter.CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        deauth = self.add("Wi-Fi Deauthentification")
        WifiDeauthFrame(deauth).pack(fill="both", expand=True)

        arp = self.add("ARP Cache Poisoning")
        dhcp = self.add("DHCP Starvation")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("SCAttack")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.geometry("800x600")
        self.minsize(500, 400)
        self.tab_view = TabView(self)
        self.tab_view.pack(fill="both", expand=True)

        self.after(100, self.result_listener)

    def result_listener(self):
        """Listen for results from the command executor"""
        while not queues.result_queue.empty():
            try:
                result = queues.result_queue.get_nowait()
            except:
                break

            self.on_result(result)
            queues.result_queue.task_done()
        # Reschedule the listener
        self.after(100, self.result_listener)

    def on_result(self, result: CommandResult):
        self.event_generate(
            id_virtual_event(
                result.command_id,
                CommandVirtualEventType.COMPLETED,
            )
        )

        match result.result:
            case None:
                pass
            case Exception as e:
                self.show_error(e)

    def show_error(self, e: Exception):
        # Create another class with CTKTopLevel and add a label
        # with the error message
        # https://customtkinter.tomschimansky.com/documentation/windows/toplevel
        pass

    def quit(self, event=None):
        self.destroy()

    def run(self):
        self.mainloop()
