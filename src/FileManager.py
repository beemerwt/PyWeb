from io import open as _open
from os.path import getsize, isfile, relpath, join, isdir
from Cacher import get_cached_file
from Config import DOCUMENT_ROOT
from Definitions import DEFAULT_FILES
# When passing path to any of these functions you MUST NOT add "DocumentRoot" to the path.


def get_absolute(path):
    path = relpath(DOCUMENT_ROOT + path)
    if isdir(path): path = next(join(path, _file) for _file in DEFAULT_FILES if isfile(DOCUMENT_ROOT + _file))
    if isfile(path): return path
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
