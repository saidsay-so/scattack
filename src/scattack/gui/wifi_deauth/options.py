from dataclasses import dataclass

from scattack.gui.utils import ETHER_ANY, ETHER_BROADCAST, BaseOptions


@dataclass
class DeauthOptions(BaseOptions):
    target_mac: str = ETHER_BROADCAST
    """MAC address of the target"""
    ap_bssid: str = ETHER_ANY
    """BSSID of the spoofed access point"""
    count: int = 0
    """Number of deauthentification packets to send, with 0 being infinite"""
