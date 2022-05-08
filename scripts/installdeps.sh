#!/usr/local/bin/bash

#
# Assumes python 3 is on PATH
# Assumes you are in a virtual environment
#
function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi

    if [[ ${areHere} = "src" ]]; then
        cd ..
    fi
}

clear
pip list > /dev/null 2>&1
STATUS=$?

if [[ ${STATUS} -eq 0 ]] ; then
    echo "in virtual environment"
    pip install --upgrade pip
    pip install wheel
    pip install -r requirements.txt
else
    echo "You are not in a virtual environment"

fi
