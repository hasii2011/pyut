#!/usr/bin/env bash

clear
echo "Clean up old stuff"
rm -rf build dist
rm -rf src/UNKNOWN.egg-info

python3 setup.py py2app -A
