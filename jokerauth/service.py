from sshjoker.settings import KEYDIR
from datetime import datetime
import os

def addNewKey(key):
    cmd = f"sudo echo '#DJANGO: {key.user} - {key.comment} - {key.create_date}\n{key.pubkey}' >> {KEYDIR}/{key.user}"
    os.system(cmd)

def deleteKey(key):
    cmd1 = f"sudo sed -i '/#DJANGO: {key.user} - {key.comment} - {key.create_date}/d' {KEYDIR}/{key.user}"
    os.system(cmd1)
    cmd2 = f"sudo sed -i '/{key.pubkey}/d' {key.user}"
    os.system(cmd2)