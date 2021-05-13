#!/bin/bash
DIR=`dirname $0`

cd $DIR/function ; ./prepare-zip.sh ; cd ..
cd $DIR/runtime ; ./prepare-zip.sh ; cd ..