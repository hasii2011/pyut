
function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "codsigning" ]]; then
        cd ../..
    fi
}


export APP=Pyut.app

xcrun stapler staple dist/${APP}
