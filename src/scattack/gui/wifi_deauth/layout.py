from dataclasses import asdict
import customtkinter
from scattack.gui.command import StopCommand, submit_command
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
        self.interval = customtkinter.CTkEntry(self, placeholder_text="0.2")
        self.interval.pack(fill="x", padx=5, pady=5)
        self.interval.bind("<FocusOut>", self.on_interval_change)

    def on_target_mac_change(self, event):
        self.options.target_mac = self.target_mac.get()

    def on_ap_bssid_change(self, event):
        self.options.ap_bssid = self.ap_bssid.get()

    def on_iface_change(self, event):
        self.options.iface = self.iface.get()

    def on_count_change(self, event):
        self.options.count = int(self.count.get())

    def on_interval_change(self, event):
        self.options.interval = float(self.interval.get())


class WifiDeauthFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = DeauthOptionsView(self)
        self.options.pack(fill="x", padx=5, pady=5)

        self.started = False
        self.action_button = customtkinter.CTkButton(
            self, text="Start", command=self.on_action_button_click
        )
        self.action_button.pack(fill="x", padx=5, pady=5)

    def on_action_button_click(self):
        if self.started:
            submit_command(StopCommand())
            self.cmd = None
            self.action_button.configure(text="Start")
            self.started = False
        else:
            self.cmd = create_deauth_command(**asdict(self.options.options), id="")
            submit_command(self.cmd)
            self.action_button.configure(text="Stop")
            self.started = True
