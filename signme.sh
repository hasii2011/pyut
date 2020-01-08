#!/usr/bin/env bash

export IDENTITY=`security find-identity -v -p codesigning | grep 'humberto.a.sanchez.ii@gmail.com' | sed -e 's/.*"\(.*\)"/\1/'`

export NAME="Pyut"
cd dist
find "${NAME}.app" -iname '*.so' -or -iname '*.dylib' |
    while read libfile; do
        codesign --sign "${IDENTITY}" \
                 --entitlements ../entitleme.plist \
                 --deep "${libfile}" \
                 --force \
                 --options runtime;
    done;


codesign --sign "${IDENTITY}" \
         --entitlements ../entitleme.plist \
         --deep "${NAME}.app" \
         --force \
         --options runtime;
