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

function checkStatus {

    status=$1
    testName=$2

    echo "checkStatus ${testName} -- ${status}"
    if [ ${status} -ne 0 ]
    then
        exit ${status}
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
cd src > /dev/null 2>&1
echo "current: `pwd`"

python3 -m tests.TestAll $*

manuallyRunSomeTests


cd -  > /dev/null 2>&1

./scripts/cleanup.sh

echo "Exit with status: ${status}"
exit ${status}

