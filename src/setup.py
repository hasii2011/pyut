#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# This file helps to create the .exe distribution.
#
# To make a .exe :
# - install py2exe
# - check this file (setup.py)
# - python setup.py py2exe
# Note: you can find py2exe at this url: py2exe.sf.net
# final .exe distribution is in dist directory
# http://starship.python.net/crew/theller/py2exe/
#
# Author : C.Dutoit 
# contact : dutoitc@hotmail.com
from distutils.core import setup
from glob import glob
import py2exe
import sys

setup(name="pyut", 
      console=["pyut.pyw"],
      data_files=[(".",
                  ["img/icon.ico"])],
    )
