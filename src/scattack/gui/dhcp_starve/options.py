__all__ = ["ARPPoisonOptions", "ETHER_ANY", "ETHER_BROADCAST", "IP_ANY"]

from dataclasses import dataclass

from scattack.gui.utils import ETHER_ANY, IP_ANY, ETHER_BROADCAST, BaseOptions


@dataclass
class ARPPoisonOptions(BaseOptions):
    target_ip: str = IP_ANY
    """IP address of the target"""
    spoofed_ip: str = IP_ANY
    """Spoofed IP address"""
    spoofed_mac: str | None = None
    """Spoofed MAC address"""
    count: int = 0
    """Number of ARP packets to send, with 0 being infinite"""
