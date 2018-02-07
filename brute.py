import paramiko
from multiprocessing.dummy import Pool as ThreadPool


def save_data(data):
    with open('valid_ssh', 'a') as valid:
        valid.write(data)


def check_ssh(ssh_item):
    host = ssh_item.split(';')[0]
    password = ssh_item.rstrip('\n').split(';')[2]

    try:
        # Trying to connect via ssh
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, port=22, username="root", password=password, timeout=20)
        ssh_client.close()
    except Exception as e:
        ssh_client.close()

    return False


def main(ssh_items, threads=2):
    pool = ThreadPool(threads)
    result = pool.map(check_ssh, ssh_items)
    pool.close()
    pool.join()
    return result


if __name__ == "__main__":
    with open('ssh.txt', 'r') as ssh_file:
        ssh_items = ssh_file.readlines()

    checked_ssh = main(ssh_items, 4)