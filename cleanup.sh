#!/bin/bash

find . -name pyutHistory"*" -exec rm -rf {} \; -print   > /dev/null
find . -name "*".log -exec rm -rf {} \; -print          > /dev/null
