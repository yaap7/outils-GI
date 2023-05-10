from os import path as os_path
from sys import path as sys_path

sys_path.insert(0, os_path.dirname(os_path.realpath(__file__)))

from app import app as application
