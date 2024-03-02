"""
author - nadav cohen
date   - 28/02/24
exercise 6.19
"""
from scapy.all import *

"""
constants
"""

TIMEOUT = 0.5


def scan_port(host, port_range):
    """
    checks if there are open ports in the given range
    :param host:
    :param port_range:
    :return: list of all the open ports
    """
    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        syn_packet = IP(dst=host) / TCP(dport=port, flags="S")
        response = sr1(syn_packet, timeout=TIMEOUT, verbose=False)
        if response is not None and response.haslayer(TCP):
            if response[TCP].flags.S and response[TCP].flags.A:
                open_ports.append(port)
    return open_ports


def main():
    host = input("what is the IP: ")
    port_range = (20, 1024)
    open_ports = scan_port(host, port_range)
    if open_ports:
        print("open ports:")
        for port in open_ports:
            print(f"\t{port}")
    else:
        print("no open ports found")


if __name__ == '__main__':
    main()
