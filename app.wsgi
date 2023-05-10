from sys import path
path.insert(0,path.dirname(path.realpath(__file__)))
print(sys.path)

from app import app as application
