from scapy.all import *
import argparse


def release_ip(src_mac, dst_mac, src_ip, dst_ip, timeout=0.2, debug=0):
    rand_xid = random.randint(1, 900000000)
    dhcp_release = ((((Ether(src=src_mac, dst=dst_mac) / IP(src=src_ip, dst=dst_ip)) / UDP(sport=68, dport=67)) / BOOTP(ciaddr=src_ip, chaddr=[mac2str(src_mac)], xid=rand_xid)) / DHCP(options=[('message-type', 'release'), ('server_id', dst_ip), ('client_id', mac2str(src_mac)), 'end']))
    sendp(dhcp_release)
    print(('Requesting release for: %s (%s)' % (src_ip, src_mac)))
    if debug:
        print(('%r' % dhcp_release))
    time.sleep(timeout)
