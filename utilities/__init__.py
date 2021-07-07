import importlib
import os
import re
import sys
from collections import namedtuple

Utility = namedtuple("utility", ["name", "description", "add_args", "run"])

_dirname = os.path.dirname(__file__)
_mod_files = [_f for _f in os.listdir(_dirname) if re.match("^util_.*\.py$", _f)]
sys.path.insert(1, _dirname)
UTILITIES = []
for _mod_file in _mod_files:
    _mod = importlib.import_module(_mod_file[:-3])
    if not all(hasattr(_mod, _attr) for _attr in ("NAME", "DESCRIPTION", "add_args", "run")):
        continue
    UTILITIES.append(Utility(_mod.NAME, _mod.DESCRIPTION, _mod.add_args, _mod.run))
sys.path.remove(_dirname)

