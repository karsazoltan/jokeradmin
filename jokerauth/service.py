from sshjoker.settings import KEYDIR


def savekeys(keys, user):
    with open(f"{KEYDIR}{user}", "w") as file:
        for key in keys:
            file.write(f"#DJANGO: {key.user} - {key.comment} - {key.create_date}\n")
            file.write(f"{key.pubkey}\n")
            file.write("\n")
