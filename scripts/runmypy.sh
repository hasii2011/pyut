#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

cd src > /dev/null 2>&1 || ! echo "No such directory"
echo "current: $(pwd)"

OPTS="--pretty --no-color-output  --show-error-context --check-untyped-defs --show-error-codes"
mypy --config-file .mypi.ini ${OPTS} pyut tests
# mypy --config-file .mypi.ini --pretty                    --show-error-codes org tests
status=$?

echo "Exit with status: ${status}"
exit ${status}

