from __future__ import absolute_import, unicode_literals

import jokerauth
from sshjoker.settings import KEYDIR
from celery import shared_task

@shared_task
def save_keys(user, active):
    keys = jokerauth.models.SSHKey.objects.filter(user__userdetail__systemuser__username=user).filter(active=active)
    with open(f"{KEYDIR}{user}", "w", encoding='utf-8') as file:
        for key in keys:
            file.write(f"# DJANGO || User: {key.user} || Comment: {key.comment} \n# Date: {key.create_date}\n")
            file.write(f"{key.pubkey}\n")
            file.write("\n")
