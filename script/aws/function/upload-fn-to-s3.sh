#!/bin/bash

PATH_TO_ROOT_DIR=$1
BUCKET_NAME=$2
FN_TAG=$3

aws s3 cp \
  "$PATH_TO_ROOT_DIR"/build/distributions/serverless-benchmark.zip \
  s3://"$BUCKET_NAME"/serverless-benchmark-"$FN_TAG".zip