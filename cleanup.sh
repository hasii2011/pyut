#!/bin/bash

find . -type f -name pyutHistory"*" -delete
find . -type f -name "*.log" -delete

cd src/tests/testdata

find . -type f -name "*.png" -delete

cd -
