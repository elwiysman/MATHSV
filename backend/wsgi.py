import sys
import os

path = '/home/elwiysman/mysite'
if path not in sys.path:
    sys.path.append(path)

from app import app as application

if __name__ == "__main__":
    application.run()