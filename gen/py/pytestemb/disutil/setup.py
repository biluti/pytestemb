
import os
import re

import setuptools
from distutils.core import setup



def find_version():
    BASE = os.path.dirname(os.path.abspath(__file__))
    VERSION_FILE = os.path.join(BASE, "../../../../src/pytestemb/__init__.py")
    with open(VERSION_FILE) as fd:
        for line in fd.read().split("\n"):
            line = re.findall(r'VERSION_STRING = "(.*?)"', line)
            if line:
               return line[0]
    raise ValueError("no version")


VERSION = find_version()
print VERSION


PACKAGES = ["pytestemb"]



setup(name="pytestemb",
      version=VERSION,
      author="jean-marc.beguinet",
      author_email="jm.beguinet@gmail.com",
      url = "https://github.com/biluti/pytestemb",
      license = "GPL",     
      packages=PACKAGES)




