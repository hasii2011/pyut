#!/bin/bash

cd src

python3 -m tests.TestAll $*
status=$?

cd ../..
find . -name pyutHistory"*" -exec rm -rf {} \; -print   > /dev/null
find . -name "*".log -exec rm -rf {} \; -print          > /dev/null


echo "Exit with status: ${status}"
exit ${status}

