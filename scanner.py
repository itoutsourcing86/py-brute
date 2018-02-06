# /usr/bin/python
# -*- coding: utf-8 -*-

import socket
import paramiko


def save_data(data):
    with open("valid.txt", "a") as f:
        f.write(data)


class Ssh_bot(object):
    def __init__(self, start_ip, end_ip, port, username, password):
        self.start_ip = start_ip
        self.end_ip = end_ip
        self.port = port
        self.username = username
        self.password = password

    def generate_hosts(self):
        start = list(map(int, self.start_ip.split(".")))
        end = list(map(int, self.end_ip.split(".")))
        temp = start
        ip_range = []

        ip_range.append(self.start_ip)
        while temp != end:
            start[3] += 1
            for i in (3, 2, 1):
                if temp[i] == 256:
                    temp[i] = 0
                    temp[i - 1] += 1
            ip_range.append(".".join(map(str, temp)))

        return ip_range

    def check_connect(self):
        try:
            cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli.settimeout(10)
            cli.connect((self.host, self.port))
            banner = cli.recv(1024)
            print("[INFO] %s\t%s"% (self.host, banner))
            return True
        except Exception as e:
            print("[ERROR] Connection is %s"% e)
            return False

    def login(self):
        try:
            ssh_cli = paramiko.SSHClient()
            ssh_cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_cli.connect(self.host, port=self.port, username=self.username, password=self.password)
            save_data("%s:%s:%s"% (self.host, self.username, self.password))
            ssh_cli.close()
        except Exception as e:
            print("[ERROR] Authentication is %s"% e)

    def run(self):
        ip_range = self.generate_hosts()
        for host in ip_range:
            print(host)


def main():
    bot = Ssh_bot("192.168.1.1", "192.168.1.254", 22, "root", "p@ssw0rd")
    bot.run()


if __name__ == '__main__':
    main()