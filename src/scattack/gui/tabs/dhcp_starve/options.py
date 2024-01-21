from dataclasses import dataclass
from scattack.core.utils import IP_ANY
from scapy.layers.l2 import Net
from scattack.gui.utils import BaseOptions


@dataclass
class DhcpStarveOptions(BaseOptions):
    net_range: str = IP_ANY + "/24"
    """Network range"""
    target_mac: str = "00:00:00:00:00:00"
    """Target MAC address"""
