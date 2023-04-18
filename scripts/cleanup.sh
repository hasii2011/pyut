#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

rm -rf dist build
rm -rf Pyut.dist Pyut.build
rm -rf Pyut.egg-info

find . -type f -name pyutHistory"*" -delete
find . -type f -name "*.log"        -delete
find . -type f -name UnitTest.gml   -delete

rm -rf UNKNOWN.egg-info
