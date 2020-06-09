#!/usr/local/bin/bash
#
#  Assumes python 3 is on PATH
#
function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

clear

pyinstaller --debug=imports --onefile --windowed  Pyut.spec

