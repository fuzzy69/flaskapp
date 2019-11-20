# -*- coding: UTF-8 -*-

from os.path import abspath, dirname, join
from time import strftime

__title__ = "Kitty Flask Demo"
__short_title__ = "kitty"
__description__ = ""
__version__ = (0, 1, 1, 191118)

version = '.'.join(map(str, __version__))
DEBUG = True
TIMESTAMP_FORMAT = "%Y-%m-%d %H-%M-%S"

# Dirs
ROOT_DIR = abspath(dirname(__file__))
APP_DIR = join(ROOT_DIR, "application")
DATA_DIR = join(ROOT_DIR, "data")
LOG_DIR = join(ROOT_DIR, "logs")
STATIC_DIR = join(ROOT_DIR, "static")
TEMPLATES_DIR = join(APP_DIR, "templates")

# Files
H5_FILE = join(DATA_DIR, "kitti.h5")
# H5_FILE = "/mnt/ramdisk/kitti.h5"
OXTS_CSV_FILE = join(DATA_DIR, "oxts.csv")

OXTS_TABLE_COLUMNS = (
    "timestamp",
    "lat", "lon", "alt", "roll", "pitch", "yaw", "vn", "ve", "vf", "vl", "vu", "ax", "ay", "az", "af", "al", "au", "wx",
    "wy", "wz", "wf", "wl", "wu", "pos_accuracy", "vel_accuracy", "navstat", "numsats", "posmode", "velmode", "orimode"
)

HOST = "127.0.0.1"  # Dev
# HOST = "0.0.0.0"  # Production
PORT = 4000
SECRET_KEY = "12345"  # TODO: move out the sensitive data

LOGGING = True
LOG_FILE = join(LOG_DIR, "webui {}.log".format(strftime(TIMESTAMP_FORMAT).replace(' ', '_')))
LOG_FORMAT = "[%(asctime)s] <%(filename)s:%(funcName)s:%(lineno)d> %(levelname)s - %(message)s", \
                   "%Y-%m-%d %H:%M:%S",
IPP = 15

USERNAME = "demo"
PASSWORD = "demo"
