__all__ = ["BaseOptions", "ETHER_ANY", "ETHER_BROADCAST", "IP_ANY"]

from dataclasses import dataclass

from scattack.core.utils import ETHER_ANY, ETHER_BROADCAST, IP_ANY


@dataclass
class BaseOptions:
    iface: str = ""
    """Interface"""
    interval: float = 0.1
    """Interval between packets"""
