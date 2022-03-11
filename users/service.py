from __future__ import absolute_import, unicode_literals

import subprocess
from celery import shared_task
from sshjoker.settings import ROOT_GROUP, HOME_DIRECTORY


def is_sudo(username):
    p = subprocess.run([f'cat /etc/group | grep {ROOT_GROUP}:'], shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return username in p.stdout.strip().split(",")


@shared_task
def adduser(username):
    """
    useradd -g fusers -m -c "$UPROJ - $NAME" -d /home1/$PROJ -u $ID $PROJ
    sacctmgr add user $PROJ Account=vik-oktatoi
    """
    try:
        subprocess.run(f"sudo useradd -g fusers -m -c \"by celery service\" -d {HOME_DIRECTORY}{username} {username}", shell=True, check=True)
        subprocess.run(f"sudo sacctmgr add user {username} Account=vik-hallgatoi", shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        return e.returncode


@shared_task
def delete_user(username):
    try:
        subprocess.run(f"sudo userdel -r {username}", shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        return e.returncode