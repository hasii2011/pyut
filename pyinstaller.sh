#!/usr/bin/env bash
#
#  Assumes python 3 is on PATH
#
clear

./cleanup.sh

pyinstaller --debug=imports --onefile --windowed  Pyut.spec

