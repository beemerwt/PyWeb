from glob import glob
from io import open
from os import remove
from os.path import isfile

from Config import DOCUMENT_ROOT
from LZ77 import LZ77Compressor

types = ("*.html", "*.htm", "*.php")
lz = LZ77Compressor()


def cache_all():
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob(DOCUMENT_ROOT + files))
    for _file in files_grabbed:
        lz.compress(_file, output_file_path=(_file + '.cache'))


def clear_cache():
    files_grabbed = glob(DOCUMENT_ROOT + "*.cache")
    for _file in files_grabbed:
        remove(_file)


def get_file(path):
    if isfile(path + ".cache"):
        return open(path + ".cache", "rb")
    return open(path, "rb")
