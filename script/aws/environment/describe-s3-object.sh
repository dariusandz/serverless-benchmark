#!/bin/bash
S3_BUCKET_NAME=$1
FN_TAG=$2

aws s3api head-object \
  --bucket "$S3_BUCKET_NAME" \
  --key serverless-benchmark-"$FN_TAG".zip