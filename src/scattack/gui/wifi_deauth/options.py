from dataclasses import dataclass

from scattack.gui.utils import BaseOptions

ETHER_BROADCAST = "ff:ff:ff:ff:ff:ff"
ETHER_ANY = "00:00:00:00:00:00"


@dataclass
class DeauthOptions(BaseOptions):
    target_mac: str = ETHER_BROADCAST
    """MAC address of the target"""
    ap_bssid: str = ETHER_ANY
    """BSSID of the spoofed access point"""
    count: int = 0
    """Number of deauthentification packets to send, with 0 being infinite"""
