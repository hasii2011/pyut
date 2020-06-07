#!/usr/bin/env bash
#
#  Assumes python 3 is on PATH
#
clear

if [[ $# -eq 0 ]] ; then
        echo "in alias mode"
        rm -rf build dist
        python3 setup.py py2app -A --iconfile src/org/pyut/resources/img/Pyut.icns
else
    if [[ ${1} = 'deploy' ]] ; then
            echo "in deploy mode"
            rm -rf build dist
            python3 setup.py py2app --packages=wx,xmlschema,pygmlparser --iconfile src/org/pyut/resources/img/Pyut.icns
    else
        echo "Unknown command line arguments"
    fi
# rm -rf src/UNKNOWN.egg-info
fi
