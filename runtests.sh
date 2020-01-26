#!/bin/bash

cd src/tests

python3 -m TestAll
status=$?

echo "Exit with status: ${status}"
exit ${status}

