#!/usr/bin/env bash

#
#  assumes Xcode 13is installed
#  assumes I added an entry APP_PASSWORD to my keychain
#
clear
xcrun notarytool log $1 --keychain-profile "APP_PASSWORD" developer_log.json
