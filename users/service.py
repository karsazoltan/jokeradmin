import subprocess
from sshjoker.settings import ROOT_GROUP, HOME_DIRECTORY


def issudo(username):
    p = subprocess.run([f'cat /etc/group | grep {ROOT_GROUP}:'], shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return username in p.stdout.strip().split(",")


def adduser(username):
    try:
        subprocess.run(f"sudo useradd -m -d {HOME_DIRECTORY}{username} {username}", shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        return e.returncode


def deluser(username):
    try:
        subprocess.run(f"sudo userdel -r {username}", shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        return e.returncode