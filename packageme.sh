#!/usr/bin/env bash

clear
echo "Clean up old stuff"
rm -rf build dist

python3 setup.py py2app --iconfile src/org/pyut/resources/img/Pyut.icns

rm -rf src/UNKNOWN.egg-info
