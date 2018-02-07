# /usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading


# Saving valid resources in the file
def save_data(data):
    with open("ssh.txt", "a") as f:
        f.write(data)


# Generating ip list from ip range
def generate_hosts(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []

    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i - 1] += 1
        ip_range.append(".".join(map(str, temp)))

    return ip_range


# Running check to open port and start threads
class Worker(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def run(self):
        self.check()

    def check(self):
        try:
            cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli.settimeout(5)
            cli.connect((self.ip, 22))
            banner = cli.recv(1024)
            print("[INFO] %s\t%s"% (self.ip, banner))
            save_data(self.ip+"\n")
        except Exception as e:
            print("[ERROR] %s\t%s"% (self.ip, e))


def main():
    ip_range = generate_hosts("62.24.75.1", "62.24.75.254")
    for ip in ip_range:
        bot = Worker(ip)
        bot.start()


if __name__ == '__main__':
    main()