from sshjoker.settings import KEYDIR


def savekeys(keys, user):
    with open(f"{KEYDIR}{user}", "w", encoding='utf-8') as file:
        for key in keys:
            file.write(f"#DJANGO: {key.user} - {key.comment} - {key.create_date}\n")
            file.write(f"{key.pubkey}\n")
            file.write("\n")
