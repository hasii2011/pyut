#!/usr/bin/env bash

export VERBOSE="--show-progress --show-scons"
export IMPORTS="--follow-imports"
export IO_PLUGINS="--include-plugin-directory=src/org/pyut/persistence"
export PYUT_PLUGINS="--include-plugin-directory=src/org/pyut/plugins"

python3 -m nuitka --clang --standalone ${VERBOSE} ${IMPORTS} src/Pyut.py

cd Pyut.dist
mkdir -p org/pyut/resources
cd ..

cp -p src/org/pyut/resources/loggingConfiguration.json Pyut.dist/org/pyut/resources
cp -p src/org/pyut/resources/Kilroy-Pyut.txt Pyut.dist/org/pyut/resources
