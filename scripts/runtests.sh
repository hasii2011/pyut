#!/bin/bash


cd src > /dev/null 2>&1


python3 -m tests.TestAll $*
status=$?

cd -  > /dev/null 2>&1

./cleanup.sh

echo "Exit with status: ${status}"
exit ${status}

