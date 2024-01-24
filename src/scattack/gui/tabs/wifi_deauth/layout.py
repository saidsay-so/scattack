from dataclasses import asdict
from tkinter import DoubleVar, IntVar, StringVar
from tkinter import ttk
from scattack.gui.command import (
    CommandCompleted,
    CommandEvent,
    CommandScheduled,
    CommandStartRequest,
    CommandStopRequest,
    TabCommandQueue,
)
from scattack.gui.validation import is_float, is_int, is_mac_address
from scattack.gui.tabs.wifi_deauth.command import create_deauth_command
from scattack.gui.tabs.wifi_deauth.options import (
    ETHER_ANY,
    ETHER_BROADCAST,
    DeauthOptions,
)

from scapy.all import conf


class DeauthOptionsView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ttk.Label(self, text="Target MAC address").pack(fill="x", padx=5, pady=5)

        self.target_mac = StringVar(value=ETHER_BROADCAST)
        self.target_mac_input = ttk.Entry(
            self,
            validatecommand=(self.register(is_mac_address), "%P"),
            validate="focus",
            textvariable=self.target_mac,
        )
        self.target_mac_input.pack(fill="x", padx=5, pady=5)

        ttk.Label(self, text="Access point BSSID").pack(fill="x", padx=5, pady=5)
        ap_bssid_validate = (self.register(is_mac_address), "%P")
        self.ap_bssid = StringVar(value=ETHER_ANY)
        self.ap_bssid_input = ttk.Entry(
            self,
            validatecommand=ap_bssid_validate,
            validate="focus",
            textvariable=self.ap_bssid,
        )
        self.ap_bssid_input.pack(fill="x", padx=5, pady=5)

        ttk.Label(self, text="Interface").pack(fill="x", padx=5, pady=5)
        self.iface = StringVar(value=next(ifa for ifa in conf.ifaces))
        self.iface_input = ttk.Combobox(
            self, textvariable=self.iface, values=tuple(ifa for ifa in conf.ifaces)
        )
        self.iface_input.pack(fill="x", padx=5, pady=5)

        ttk.Label(self, text="Count").pack(fill="x", padx=5, pady=5)
        count_validate = (self.register(is_int), "%P")
        self.count = IntVar(value=0)
        self.count_input = ttk.Entry(
            self,
            validate="all",
            validatecommand=count_validate,
            textvariable=self.count,
        )
        self.count_input.pack(fill="x", padx=5, pady=5)

        ttk.Label(self, text="Interval").pack(fill="x", padx=5, pady=5)
        interval_validate = (self.register(is_float), "%P")
        self.interval = DoubleVar(value=0.1)
        self.interval_input = ttk.Entry(
            self,
            validate="all",
            validatecommand=interval_validate,
            textvariable=self.interval,
        )
        self.interval_input.pack(fill="x", padx=5, pady=5)


class WifiDeauthFrame(ttk.Frame):
    def __init__(self, *args, queue: TabCommandQueue, **kwargs):
        super().__init__(*args, **kwargs)
        self.options_view = DeauthOptionsView(self)
        self.options_view.pack(fill="x", padx=5, pady=5)
        self.cmd_queue = queue

        self.cmd_id = None
        self.started = False
        self.action_text = StringVar(value="Start")
        self.action_button = ttk.Button(
            self, textvariable=self.action_text, command=self.on_action_button_click
        )
        self.action_button.pack(fill="x", padx=5, pady=5)

    def on_action_button_click(self):
        if not self.started and self.cmd_id is not None:
            return

        if self.started and self.cmd_id:
            self.cmd_queue.put(CommandStopRequest(self.cmd_id))
        else:
            options = DeauthOptions(
                target_mac=self.options_view.target_mac.get(),
                ap_bssid=self.options_view.ap_bssid.get(),
                iface=self.options_view.iface.get(),
                count=self.options_view.count.get(),
                interval=self.options_view.interval.get(),
            )
            cmd = create_deauth_command(**asdict(options))
            req = CommandStartRequest(callback=self.on_command_result, **cmd)
            self.cmd_id = req.command_id
            self.cmd_queue.put(req)

    def on_command_result(self, ev: CommandEvent):
        match ev:
            case CommandCompleted(id, result):
                self.cmd_id = None
                self.action_text.set("Start")
                self.started = False
            case CommandScheduled(id):
                self.action_text.set("Stop")
                self.started = True
