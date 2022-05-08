#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi

    if [[ ${areHere} = "src" ]]; then
        cd ..
    fi
}

changeToProjectRoot

REPO_SLUG='hasii2011/PyUt'
VERSION_FILE='src/org/pyut/resources/version.txt'

traviscli  --repo-slug ${REPO_SLUG} --file ${VERSION_FILE}

STATUS=$?

exit ${STATUS}
