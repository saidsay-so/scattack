from dataclasses import dataclass

ETHER_BROADCAST = "ff:ff:ff:ff:ff:ff"
ETHER_ANY = "00:00:00:00:00:00"


@dataclass
class DeauthOptions:
    target_mac: str = ETHER_BROADCAST
    """MAC address of the target"""
    ap_bssid: str = ETHER_ANY
    """BSSID of the spoofed access point"""
    iface: str = "wlan0"
    """Interface on which the deauthentification packets will be sent"""
    count: int = 0
    """Number of deauthentification packets to send, with 0 being infinite"""
    interval: float = 0.2
    """Interval between each deauthentification packet"""
