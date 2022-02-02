#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

cd src > /dev/null 2>&1
echo "current: `pwd`"

# mypy --config-file .mypi.ini --pretty --no-color-output  --show-error-codes Pyut.py
mypy --config-file .mypi.ini --pretty  --show-error-codes Pyut.py
status=$?

echo "Exit with status: ${status}"
exit ${status}

