from ..constants import DEFAULT_LOGO


def get_image(name):
    if name:
        return f"https://avatars.dicebear.com/api/initials/{name[0]}.svg"
    else:
        return DEFAULT_LOGO
