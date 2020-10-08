#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi

    if [[ ${areHere} = "src" ]]; then
        cd ..
    fi
}

changeToProjectRoot

echo "Travis Build directory: ${TRAVIS_BUILD_DIR}"
cd src > /dev/null 2>&1
echo "current: `pwd`"

python3 -m tests.TestAll $*
status=$?

cd -  > /dev/null 2>&1

./scripts/cleanup.sh

echo "Exit with status: ${status}"
exit ${status}

