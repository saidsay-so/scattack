from time import sleep
from scattack.core.wifi_deauth import create_deauth_packet, send_deauth_packet
from scattack.gui.command import Command, CommandId, StartCommand


def create_deauth_command(
    *,
    id: CommandId,
    target_mac: str,
    ap_bssid: str,
    iface: str,
    count: int,
    interval: float,
) -> Command:
    def send(*args, interval: float = interval, **kwargs):
        send_deauth_packet(*args, **kwargs)
        sleep(interval)

    def condition():
        nonlocal count
        if count == 0:
            return False
        else:
            return True

    pkt = create_deauth_packet(target_mac=target_mac, ap_bssid=ap_bssid)

    return StartCommand(
        id,
        send,
        (pkt, iface),
        {"interval": interval},
        condition if count != 0 else lambda: True,
    )
