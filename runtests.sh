#!/bin/bash

cd src

python3 -m tests.TestAll $*
status=$?

cd ..
./cleanup.sh

echo "Exit with status: ${status}"
exit ${status}

