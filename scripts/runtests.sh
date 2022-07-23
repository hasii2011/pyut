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

function manuallyRunSomeTests {

  python3 -m unittest tests.TestUmlFrame.TestUmlFrame.testClassCreation
  status=$?
  checkStatus ${status} testClassCreation

  python3 -m unittest tests.TestUmlFrame.TestUmlFrame.testNoteCreation
  status=$?
  checkStatus ${status} testNoteCreation

  python3 -m unittest tests.TestUmlFrame.TestUmlFrame.testActorCreation
  status=$?
  checkStatus ${status} testActorCreation

  python3 -m unittest tests.TestUmlFrame.TestUmlFrame.testUseCaseCreation
  status=$?
  checkStatus ${status} testUseCaseCreation

}
changeToProjectRoot

echo "Travis Build directory: ${TRAVIS_BUILD_DIR}"
cd src > /dev/null 2>&1  || ! echo "No such directory"
echo "current: $(pwd)"

python -m tests.TestAll
status=$?

manuallyRunSomeTests

cd -  > /dev/null 2>&1 || ! echo "No such directory"

./scripts/cleanup.sh

echo "Exit with status: ${status}"
exit ${status}

