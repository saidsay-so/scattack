from dataclasses import dataclass


@dataclass
class BaseOptions:
    iface: str = ""
    """Interface"""
    interval: float = 0.1
    """Interval between packets"""
