from dataclasses import asdict
from tkinter import DoubleVar, IntVar, StringVar
from tkinter import ttk
from scattack.gui.tabs.arp_poison.command import create_arppoison_command
from scattack.gui.command import (
    CommandCompleted,
    CommandEvent,
    CommandScheduled,
    CommandStartRequest,
    CommandStopRequest,
    TabCommandQueue,
)
from scattack.gui.validation import is_float, is_int, is_ip_address, is_mac_address
from scattack.gui.tabs.arp_poison.options import (
    ETHER_ANY,
    ETHER_BROADCAST,
    IP_ANY,
    ARPPoisonOptions,
)

from scapy.all import conf


class ArpPoisonOptionsView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ttk.Label(self, text="Spoofed MAC address").pack(fill="x", padx=5, pady=5)
        self.spoofed_mac = StringVar(value="")
        self.spoofed_mac_input = ttk.Entry(
            self,
            validatecommand=(self.register(is_mac_address), "%P"),
            validate="focus",
            textvariable=self.spoofed_mac,
        )
        self.spoofed_mac_input.pack(fill="x", padx=5, pady=5)

        ttk.Label(self, text="Target IP").pack(fill="x", padx=5, pady=5)
        target_ip_validate = (self.register(is_ip_address), "%P")
        self.target_ip = StringVar(value=IP_ANY)
        self.target_ip_input = ttk.Entry(
            self,
            validatecommand=target_ip_validate,
            validate="focus",
            textvariable=self.target_ip,
        )
        self.target_ip_input.pack(fill="x", padx=5, pady=5)

        ttk.Label(self, text="Spoofed IP").pack(fill="x", padx=5, pady=5)
        spoofed_ip_validate = (self.register(is_ip_address), "%P")
        self.spoofed_ip = StringVar(value=IP_ANY)
        self.spoofed_ip_input = ttk.Entry(
            self,
            validatecommand=spoofed_ip_validate,
            validate="focus",
            textvariable=self.spoofed_ip,
        )
        self.spoofed_ip_input.pack(fill="x", padx=5, pady=5)

        ttk.Label(self, text="Interface").pack(fill="x", padx=5, pady=5)
        self.iface = StringVar()
        self.iface_input = ttk.Combobox(
            self, textvariable=self.iface, values=conf.ifaces
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


class ArpPoisonFrame(ttk.Frame):
    def __init__(self, *args, queue: TabCommandQueue, **kwargs):
        super().__init__(*args, **kwargs)
        self.options_view = ArpPoisonOptionsView(self)
        self.options_view.pack(fill="x", padx=5, pady=5)
        self.cmd_queue = queue

        self.cmd_id = None
        self.started = False
        self.action_button = ttk.Button(
            self, text="Start", command=self.on_action_button_click
        )
        self.action_button.pack(fill="x", padx=5, pady=5)

    def on_action_button_click(self):
        if not self.started and self.cmd_id is not None:
            return

        if self.started and self.cmd_id:
            self.cmd_queue.put(CommandStopRequest(self.cmd_id))
        else:
            options = ARPPoisonOptions(
                target_ip=self.options_view.target_ip.get(),
                spoofed_ip=self.options_view.spoofed_ip.get(),
                spoofed_mac=self.options_view.spoofed_mac.get()
                if self.options_view.spoofed_mac.get() != ""
                else None,
                iface=self.options_view.iface.get(),
                count=self.options_view.count.get(),
                interval=self.options_view.interval.get(),
            )
            cmd = create_arppoison_command(**asdict(options))
            req = CommandStartRequest(callback=self.on_command_result, **cmd)
            self.cmd_id = req.command_id
            self.cmd_queue.put(req)

    def on_command_result(self, ev: CommandEvent):
        match ev:
            case CommandCompleted(id, result):
                self.cmd_id = None
                self.action_button.configure(text="Start")
                self.started = False
            case CommandScheduled(id):
                self.action_button.configure(text="Stop")
                self.started = True
