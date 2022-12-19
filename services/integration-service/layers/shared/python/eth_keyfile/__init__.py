from __future__ import absolute_import

import pkg_resources
import warnings
import sys

from eth_keyfile.keyfile import (  # noqa: F401
    load_keyfile,
    create_keyfile_json,
    decode_keyfile_json,
    extract_key_from_keyfile,
)


if sys.version_info.major < 3:
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn(DeprecationWarning(
        "The `eth-keyfile` library is dropping support for Python 2.  Upgrade to Python 3."
    ))
    warnings.resetwarnings()


try:
    __version__ = pkg_resources.get_distribution("eth-keyfile").version
except pkg_resources.DistributionNotFound:
    # package is not installed
    __version__ = None
