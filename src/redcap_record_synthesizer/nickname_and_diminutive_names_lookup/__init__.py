"""
REDCap Record Synthesizer

Class NicknameGenerator, which lets us translate "Robert" to "Bob", etc.
"""

import os


# https://stackoverflow.com/a/5423147
_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    """Returns path of data file stored in this directory.

    Parameters
    ----------
    path : str

    Returns
    -------
    str
    """
    return os.path.join(_ROOT, path)
