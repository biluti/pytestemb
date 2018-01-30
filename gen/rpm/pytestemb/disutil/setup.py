

import re
import os
import setuptools
from distutils.core import setup




def find_version():
    BASE = os.path.dirname(os.path.abspath(__file__))
    VERSION_FILE = os.path.normpath(os.path.join(BASE, "pytestemb/__init__.py"))
    
    with open(VERSION_FILE) as fd:
        for line in fd.read().split("\n"):
            line = re.findall(r'VERSION_STRING = "(.*?)"', line)
            if line:
               return line[0]
    raise ValueError("no version")



VERSION = find_version()
print VERSION

PACKAGES = setuptools.find_packages()

print PACKAGES



setup(name='pytestemb',
    version=VERSION,
    description='',
    url='',
    author='jean-marc',
    author_email='jm.beguinet@gmail.com',
    license='',
    packages=PACKAGES,
    zip_safe=False,
     )








