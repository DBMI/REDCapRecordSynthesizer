

import os
import redcap_record_synthesizer

# https://stackoverflow.com/a/5423147
_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, 'data', path)
