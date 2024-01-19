from dataclasses import dataclass

ETHER_BROADCAST = "ff:ff:ff:ff:ff:ff"
ETHER_ANY = "00:00:00:00:00:00"
IP_ANY = "0.0.0.0"


@dataclass
class ARPPoisonOptions:
    target_mac: str = ETHER_ANY
    """MAC address of the target"""
    target_ip: str = IP_ANY
    """IP address of the target"""
    spoofed_ip: str = IP_ANY
    """Spoofed IP address"""
    spoofed_mac: str = ETHER_ANY
    """Spoofed MAC address"""
