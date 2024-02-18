# scattack

Scattack was created to demonstrate the use of Scapy to perform Wifi deauthentication, ARP cache poisoning and DHCP Starvation attacks.
It is inspired by several github repos and aims to create a single platform to launch several attacks.

The implemented attacks are:

- Wifi deauthentication, using the `scapy.layers.dot11` module to send deauthentication packets to a target access point.
- ARP cache poisoning, using the `scapy.layers.l2` module to send ARP packets to a target host.
- DHCP Starvation, using the `scapy.layers.dhcp` module to send DHCP requests to a target DHCP server.
