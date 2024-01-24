from dataclasses import asdict
from tkinter import DoubleVar, StringVar
from tkinter import ttk
from scattack.core.utils import ETHER_ANY, IP_ANY
from scattack.gui.command import (
    CommandCompleted,
    CommandEvent,
    CommandScheduled,
    CommandStartRequest,
    CommandStopRequest,
    TabCommandQueue,
)
from scattack.gui.tabs.dhcp_starve.command import create_dhcp_stave_command
from scattack.gui.tabs.dhcp_starve.options import DhcpStarveOptions
from scattack.gui.validation import (
    is_float,
    is_ip_network,
    is_mac_address,
)
from scapy.config import conf
from scapy.layers.l2 import Net


class DhcpStarveOptionsView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ttk.Label(self, text="Network range").pack(fill="x", padx=5, pady=5)
        ap_bssid_validate = (self.register(is_ip_network), "%P")
        self.net_range = StringVar(value=IP_ANY + "/24")
        self.net_range_input = ttk.Entry(
            self,
            validatecommand=ap_bssid_validate,
            validate="focus",
            textvariable=self.net_range,
        )
        self.net_range_input.pack(fill="x", padx=5, pady=5)

        def num_hosts_listener(*_):
            if not self.net_range.get() or not is_ip_network(self.net_range.get()):
                return

            num_hosts_text.set(f"Number of hosts: {Net(self.net_range.get()).count}")

        num_hosts_text = StringVar(
            value=f"Number of hosts: {Net(self.net_range.get()).count}"
        )
        self.net_range.trace_add(
            "write",
            num_hosts_listener,
        )
        ttk.Label(self, textvariable=num_hosts_text).pack(fill="x", padx=5, pady=2)

        ttk.Label(self, text="Target MAC address").pack(fill="x", padx=5, pady=5)
        self.target_mac = StringVar(value=ETHER_ANY)
        self.target_mac_input = ttk.Entry(
            self,
            validatecommand=(self.register(is_mac_address), "%P"),
            validate="focus",
            textvariable=self.target_mac,
        )
        self.target_mac_input.pack(fill="x", padx=5, pady=5)

        ttk.Label(self, text="Interface").pack(fill="x", padx=5, pady=5)
        self.iface = StringVar(value=next(ifa for ifa in conf.ifaces))
        self.iface_input = ttk.Combobox(
            self, textvariable=self.iface, values=tuple(ifa for ifa in conf.ifaces)
        )
        self.iface_input.pack(fill="x", padx=5, pady=5)

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


class DhcpStarveFrame(ttk.Frame):
    def __init__(self, *args, queue: TabCommandQueue, **kwargs):
        super().__init__(*args, **kwargs)
        self.options_view = DhcpStarveOptionsView(self)
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
            options = DhcpStarveOptions(
                net_range=self.options_view.net_range.get(),
                target_mac=self.options_view.target_mac.get(),
                iface=self.options_view.iface.get(),
                interval=self.options_view.interval.get(),
            )
            cmd = create_dhcp_stave_command(**asdict(options))
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
