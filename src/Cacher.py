import gzip
import shutil
from glob import glob
from hashlib import md5
from os import remove
from os.path import isfile

from Config import DOCUMENT_ROOT
from Definitions import CHECKSUMS

types = ("*.html", "*.htm", "*.php")


def get_cached_file(path):
    if is_cached(path): return path + ".gz"
    else: compress(path)
    return path + '.gz'


def get_checksum(path):
    if path is None: return
    print "Getting checksum of:", path
    path = get_cached_file(path)
    if path in CHECKSUMS: return CHECKSUMS[path]
    c = md5(open(path, 'rb').read()).hexdigest()
    CHECKSUMS[path] = c
    return CHECKSUMS[path]


def compress(path):
    print "Creating cache of file:", path
    with open(path, 'rb') as f_in, gzip.open(path + '.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def decompress(path):
    with gzip.open(path, 'rb') as f:
        file_content = f.read()
        print file_content


def cache_all():
    print "Caching all resources in", DOCUMENT_ROOT
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob(DOCUMENT_ROOT + files))
    for _file in files_grabbed:
        if not is_cached(_file):  # If we already have it cached, don't re-cache. Use clear_cache to force
            compress(_file)


def clear_cache():
    files_grabbed = glob(DOCUMENT_ROOT + "*.gz")
    for _file in files_grabbed:
        remove(_file)


def is_cached(path):
    if path is None: return False
    return isfile(path + ".gz")
