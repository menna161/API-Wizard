import logging
from scapy.all import *
import argparse


def dhcp_discover(dst_mac='ff:ff:ff:ff:ff:ff', debug=False):
    myxid = random.randint(1, 900000000)
    src_mac = get_if_hwaddr(conf.iface)
    bogus_mac_address = RandMAC()
    options = [('message-type', 'discover'), ('max_dhcp_size', 1500), ('client_id', mac2str(bogus_mac_address)), ('lease_time', 10000), ('end', bytes('00000000000000', encoding='ascii'))]
    dhcp_request = ((((Ether(src=src_mac, dst=dst_mac) / IP(src='0.0.0.0', dst='255.255.255.255')) / UDP(sport=68, dport=67)) / BOOTP(chaddr=[mac2str(bogus_mac_address)], xid=myxid, flags=16777215)) / DHCP(options=options))
    sendp(dhcp_request, iface=conf.iface)
