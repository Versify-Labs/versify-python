import pkg_resources

from eth_abi.abi import (  # NOQA
    decode_single,
    decode_abi,
    encode_single,
    encode_abi,
)


try:
    __version__ = pkg_resources.get_distribution("eth-abi").version
except pkg_resources.DistributionNotFound:
    # package is not installed
    __version__ = None
