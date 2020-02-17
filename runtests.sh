#!/bin/bash

cd src/tests

python3 -m TestAll $*
status=$?

cd ..
find . -name pyutHistory"*" -exec rm -rf {} \; -print
find . -name "*".log -exec rm -rf {} \; -print


echo "Exit with status: ${status}"
exit ${status}

