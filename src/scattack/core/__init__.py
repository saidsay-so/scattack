from scapy.packet import Packet
from scapy.sendrecv import sendp


def send_packet(pkt: Packet, iface: str) -> None:
    """Send Layer 2 packet.

    Args:
        pkt (Packet): Packet to send
        iface (str): name of the interface to send the packet on
    Returns:
        None"""
    return sendp(pkt, iface=iface, verbose=False)
