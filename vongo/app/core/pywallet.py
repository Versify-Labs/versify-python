import inspect
from datetime import datetime

from .utils import HDKey, HDPrivateKey


def generate_mnemonic(strength=128):
    _, seed = HDPrivateKey.master_key_from_entropy(strength=strength)
    return seed


def generate_child_id():
    now = datetime.now()
    seconds_since_midnight = (
        now - now.replace(hour=0, minute=0, second=0, microsecond=0)
    ).total_seconds()
    return int((int(now.strftime("%y%m%d")) + seconds_since_midnight * 1000000) // 100)


def create_address(xpub=None, child=None, path=0):
    assert xpub is not None

    if child is None:
        child = generate_child_id()

    acct_pub_key = HDKey.from_b58check(xpub)

    keys = HDKey.from_path(
        acct_pub_key, "{change}/{index}".format(change=path, index=child)
    )

    res = {
        "path": "m/" + str(acct_pub_key.index) + "/" + str(keys[-1].index),
        "bip32_path": "m/44'/60'/0'/"
        + str(acct_pub_key.index)
        + "/"
        + str(keys[-1].index),
        "address": keys[-1].address(),
    }

    if inspect.stack()[1][3] == "create_wallet":
        res["xpublic_key"] = keys[-1].to_b58check()

    return res


def create_wallet(seed=None, children=1):

    if seed is None:
        seed = generate_mnemonic()

    wallet = {
        "coin": "ETH",
        "seed": seed,
        "private_key": "",
        "public_key": "",
        "xprivate_key": "",
        "xpublic_key": "",
        "address": "",
        "wif": "",
        "children": [],
    }

    master_key = HDPrivateKey.master_key_from_mnemonic(seed)
    root_keys = HDKey.from_path(master_key, "m/44'/60'/0'")

    acct_priv_key = root_keys[-1]
    acct_pub_key = acct_priv_key.public_key

    wallet["private_key"] = acct_priv_key.to_hex()
    wallet["public_key"] = acct_pub_key.to_hex()
    wallet["xprivate_key"] = acct_priv_key.to_b58check()
    wallet["xpublic_key"] = acct_pub_key.to_b58check()

    child_wallet = create_address(xpub=wallet["xpublic_key"], child=0, path=0)
    wallet["address"] = child_wallet["address"]
    wallet["xpublic_key_prime"] = child_wallet["xpublic_key"]

    # get public info from first prime child
    for child in range(children):
        child_wallet = create_address(xpub=wallet["xpublic_key"], child=child, path=0)
        wallet["children"].append(
            {
                "address": child_wallet["address"],
                "xpublic_key": child_wallet["xpublic_key"],
                "path": "m/" + str(child),
                "bip32_path": "m/44'/60'/0'/" + str(child),
            }
        )

    return wallet
