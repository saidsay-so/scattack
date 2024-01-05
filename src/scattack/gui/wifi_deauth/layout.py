from dataclasses import asdict
import customtkinter
from scattack.gui.command import (
    CommandCompleted,
    CommandEvent,
    CommandScheduled,
    CommandStartRequest,
    CommandStopRequest,
    StopCommand,
    TabCommandQueue,
)
from scattack.gui.wifi_deauth.command import create_deauth_command

from scattack.gui.wifi_deauth.utils import DeauthOptions


class DeauthOptionsView(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = DeauthOptions()

        customtkinter.CTkLabel(self, text="Target MAC address").pack(
            fill="x", padx=5, pady=5
        )
        self.target_mac = customtkinter.CTkEntry(
            self, placeholder_text="ff:ff:ff:ff:ff:ff"
        )
        self.target_mac.pack(fill="x", padx=5, pady=5)
        self.target_mac.bind("<FocusOut>", self.on_target_mac_change)

        customtkinter.CTkLabel(self, text="Access point BSSID").pack(
            fill="x", padx=5, pady=5
        )
        self.ap_bssid = customtkinter.CTkEntry(
            self, placeholder_text="00:00:00:00:00:00"
        )
        self.ap_bssid.pack(fill="x", padx=5, pady=5)
        self.ap_bssid.bind("<FocusOut>", self.on_ap_bssid_change)

        customtkinter.CTkLabel(self, text="Interface").pack(fill="x", padx=5, pady=5)
        self.iface = customtkinter.CTkEntry(self, placeholder_text="wlan0")
        self.iface.pack(fill="x", padx=5, pady=5)
        self.iface.bind("<FocusOut>", self.on_iface_change)

        customtkinter.CTkLabel(self, text="Count").pack(fill="x", padx=5, pady=5)
        self.count = customtkinter.CTkEntry(self, placeholder_text="0")
        self.count.pack(fill="x", padx=5, pady=5)
        self.count.bind("<FocusOut>", self.on_count_change)

        customtkinter.CTkLabel(self, text="Interval").pack(fill="x", padx=5, pady=5)
        self.interval = customtkinter.CTkEntry(self, placeholder_text="0.1")
        self.interval.pack(fill="x", padx=5, pady=5)
        self.interval.bind("<FocusOut>", self.on_interval_change)

    def on_target_mac_change(self, event):
        self.options.target_mac = self.target_mac.get()

    def on_ap_bssid_change(self, event):
        self.options.ap_bssid = self.ap_bssid.get()

    def on_iface_change(self, event):
        self.options.iface = self.iface.get()

    def on_count_change(self, event):
        if self.count.get():
            self.options.count = int(self.count.get())

    def on_interval_change(self, event):
        if self.interval.get():
            self.options.interval = float(self.interval.get())


class WifiDeauthFrame(customtkinter.CTkFrame):
    def __init__(self, *args, queue: TabCommandQueue, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = DeauthOptionsView(self)
        self.options.pack(fill="x", padx=5, pady=5)
        self.cmd_queue = queue

        self.cmd_id = None
        self.started = False
        self.action_button = customtkinter.CTkButton(
            self, text="Start", command=self.on_action_button_click
        )
        self.action_button.pack(fill="x", padx=5, pady=5)

    def on_action_button_click(self):
        if not self.started and self.cmd_id is not None:
            return

        if self.started and self.cmd_id:
            self.cmd_queue.put(CommandStopRequest(self.cmd_id))
        else:
            cmd = create_deauth_command(**asdict(self.options.options))
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
