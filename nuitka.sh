#!/usr/bin/env bash

rm -rf Pyut.dist
rm -rf Pyut.build

export VERBOSE="--show-progress --show-scons"
export IMPORTS="--follow-imports"
export IO_PLUGINS="--include-plugin-directory=src/org/pyut/persistence"
export PYUT_PLUGINS="--include-plugin-directory=src/org/pyut/plugins"

export OTHER_OPTS="--standalone"

python3 -m nuitka --clang --standalone ${VERBOSE} ${IO_PLUGINS} ${PYUT_PLUGINS} ${IMPORTS} ${OTHER_OPTS} src/Pyut.py

cd Pyut.dist
mkdir -p org/pyut/resources
cd ..

cp -p src/org/pyut/resources/loggingConfiguration.json Pyut.dist/org/pyut/resources
cp -p src/org/pyut/resources/Kilroy-Pyut.txt Pyut.dist/org/pyut/resources
