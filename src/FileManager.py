from io import open as _open
from os.path import getsize, isfile, relpath

from Cacher import get_cached_file
from Config import DOCUMENT_ROOT
from Definitions import DEFAULT_FILES


def get_safe(path):
    if path.endswith("/"): return next(_file for _file in DEFAULT_FILES if isfile(DOCUMENT_ROOT + _file))
    if isfile(relpath(DOCUMENT_ROOT + path)): return path[1:]  # get rid of the slash in front of the path.
    return None


def size(path):
    path = get_cached_file(path)
    return getsize(path)


def open(path):
    path = get_cached_file(path)
    return _open(path, "rb")


def check(path):
    if path is None: return 404
    return 200