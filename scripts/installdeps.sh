#!/usr/local/bin/bash

#
# Assumes python 3 is on PATH
# Assumes you are in a virtual environment
#
function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi

    if [[ ${areHere} = "src" ]]; then
        cd ..
    fi
}

clear
pip3 list > /dev/null 2>&1
STATUS=$?

if [[ ${STATUS} -eq 0 ]] ; then
    echo "in virtual environment"
    pip3 install --upgrade pip
    pip3 install wheel
    pip3 install -r requirements.txt
else
    echo "You are not in a virtual environment"

fi
