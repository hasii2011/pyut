#!/usr/bin/env bash
#
#  Assumes python 3 is on PATH
#
clear

./cleanup.sh

pyinstaller --onefile --windowed -d all Pyut.spec

