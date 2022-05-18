#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

cd src > /dev/null 2>&1
echo "current: $(pwd)"

mypy --config-file .mypi.ini --pretty --no-color-output  --show-error-codes org pyutmodel tests
# mypy --config-file .mypi.ini --pretty                    --show-error-codes org pyutmodel tests
status=$?

echo "Exit with status: ${status}"
exit ${status}

