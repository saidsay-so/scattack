from scapy.packet import Packet
from scapy.sendrecv import sendp


def send_packet(pkt: Packet, iface: str) -> None:
    """Send 802.11 deauthentification packet.

    Args:
        pkt (Packet): 802.11 deauthentification packet
        iface (str): name of the interface to send the packet on
    Returns:
        None"""
    return sendp(pkt, iface=iface, verbose=False)
