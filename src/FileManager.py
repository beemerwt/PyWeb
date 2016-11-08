from io import open as _open
from os.path import getsize, isfile

from Cacher import is_cached, compress
from Config import DOCUMENT_ROOT
from Definitions import DEFAULT_FILES


# When passing path to any of these functions you MUST NOT add "DocumentRoot" to the path.


def __get_absolute(path):
    if not isfile(DOCUMENT_ROOT + path):
        path = DOCUMENT_ROOT + next(_file for _file in DEFAULT_FILES if isfile(DOCUMENT_ROOT + _file))
    return DOCUMENT_ROOT + path


def size(path):
    path = __get_absolute(path)
    if not is_cached(path):
        compress(path)
    return getsize(path + ".gz")


def open(path):
    path = __get_absolute(path)
    if is_cached(path):
        return _open(path + ".gz", "rb")
    compress(path)
    return _open(path + ".gz", "rb")


def check(path):
    if path == "/":
        for name in DEFAULT_FILES:
            if isfile(DOCUMENT_ROOT + name):
                return 200
    path = path.replace("/", "", 1)  # Remove first occurrence of "/"
    if isfile(DOCUMENT_ROOT + path):
        return 200
    return 404
