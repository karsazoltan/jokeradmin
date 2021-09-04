import subprocess

from sshjoker.settings import ROOT_GROUP

def issudo(username):
    p = subprocess.run([f'cat /etc/group | grep {ROOT_GROUP}'], shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return username in p.stdout
