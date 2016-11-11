import gzip
import shutil
from distutils.dir_util import mkpath
from glob import glob
from hashlib import md5
from os import remove
from os.path import isfile, relpath, isdir, dirname

from Config import DOCUMENT_ROOT, CACHE_ROOT
from Definitions import CHECKSUMS


def get_cached_file(_file):
    if is_cached(_file):
        return relpath(CACHE_ROOT + _file + ".gz")
    else:
        compress(_file)
    return relpath(CACHE_ROOT + _file + '.gz')


def get_checksum(path):
    if path is None: return
    path = get_cached_file(path)
    if path in CHECKSUMS: return CHECKSUMS[path]
    c = md5(open(path, 'rb').read()).hexdigest()
    CHECKSUMS[path] = c
    return CHECKSUMS[path]


def compress(_file):
    print "Creating cache of file:", _file
    if not isdir(CACHE_ROOT + _file):
        mkpath(dirname(CACHE_ROOT + _file))
    with open(relpath(DOCUMENT_ROOT + _file), 'rb') as f_in, gzip.open(CACHE_ROOT + _file + '.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def decompress(_file):
    with gzip.open(CACHE_ROOT + _file, 'rb') as f:
        file_content = f.read()
        print file_content


def cache_all():
    print "Caching all resources in", CACHE_ROOT
    files_grabbed = []
    d_root_length = DOCUMENT_ROOT.__len__()
    files_grabbed.extend(glob(DOCUMENT_ROOT + "*.*"))
    for _file in files_grabbed:
        super_path = relpath(_file)[d_root_length:]
        if not is_cached(super_path):  # If we already have it cached, don't re-cache. Use clear_cache to force
            compress(super_path)


def clear_cache():
    files_grabbed = glob(CACHE_ROOT + "*.gz")
    for _file in files_grabbed:
        remove(_file)


def is_cached(_file):
    if _file is None: return False
    return isfile(CACHE_ROOT + _file + ".gz")
