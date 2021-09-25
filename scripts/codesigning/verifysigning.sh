#!/usr/bin/env bash

#
#  assumes Xcode 13 is installed
#  assumes I added an entry APP_PASSWORD to my keychain
#

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    echo ${areHere}
    if [[ ${areHere} = "codesigning" ]]; then
        cd ../..
    fi
}
#
#  assumes xcode is installed
#

changeToProjectRoot

spctl -vvvv --assess --type exec dist/Pyut.app
