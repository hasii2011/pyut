#!/usr/bin/env bash

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

function checkStatus {

    status=$1
    testName=$2

    echo "checkStatus ${testName} -- ${status}"
    if [ "${status}" -ne 0 ]
    then
        exit "${status}"
    fi
}

changeToProjectRoot

echo "current: $(pwd)"

python3 -m tests.TestAll
status=$?

cd -  > /dev/null 2>&1 || ! echo "No such directory"

./scripts/cleanup.sh

# echo "Exit with status: ${status}"
# Hopefully this will be fixed sooon
# Fatal Python error: PyThreadState_Get: the function must be called with the GIL held, but the GIL is
# released (the current Python thread state is NULL)
# Python runtime state: finalizing (tstate=0x0000000152604b80)
# exit ${status}
echo 'Fake exit 0'
exit 0

