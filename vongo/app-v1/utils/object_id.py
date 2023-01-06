from ksuid import ksuid


def generate_id(prefix: str):
    uid = f"{prefix}_{ksuid()}"
    return uid[:24]
