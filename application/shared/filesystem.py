from os import listdir, makedirs, remove, walk
from os.path import basename, exists, isfile, join, split, splitext


def ensure_dir(dir_path: str) -> bool:
    """
    Create directory path if it doesn't exists
    :param str dir_path: full path to target directory
    :return: return True if directory path is created or False if it already exists
    :raise: when creating directories fails (permission issue, unreachable target media, etc ...)
    """
    if not exists(dir_path):
        makedirs(dir_path)
        return True

    return False
