from ipaddress import ip_address, ip_network
from re import match


def is_mac_address(mac_address: str) -> bool:
    """Check if the input is a valid MAC address.

    Args:
        mac_address (str): MAC address

    Returns:
        bool: True if the input is a valid MAC address, False otherwise"""
    return bool(match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac_address))


def is_ip_address(addr: str) -> bool:
    """Check if the input is a valid IP address.

    Args:
        addr (str): IP address

    Returns:
        bool: True if the input is a valid IP address, False otherwise"""
    try:
        ip_address(addr)
        return True
    except ValueError:
        return False


def is_ip_network(addr: str) -> bool:
    """Check if the input is a valid IP network.

    Args:
        addr (str): IP network

    Returns:
        bool: True if the input is a valid IP network, False otherwise"""
    try:
        ip_network(addr)
        return True
    except ValueError:
        return False


def is_int(value: str) -> bool:
    """Check if the input is a valid integer.

    Args:
        value (str): Integer

    Returns:
        bool: True if the input is a valid integer, False otherwise"""
    return value.isdecimal()


def is_float(value: str) -> bool:
    """Check if the input is a valid float.

    Args:
        value (str): Float

    Returns:
        bool: True if the input is a valid float, False otherwise"""
    return value.replace(".", "", 1).isdecimal()
