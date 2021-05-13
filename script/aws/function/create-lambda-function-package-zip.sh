#!/bin/bash
FUNCTION_NAME=$1
FUNCTION_MEMORY_SIZE=$2
AWS_ROLE_ARN=$3
RUNTIME=$4
BUCKET_NAME=$5
FN_TAG=$6

aws lambda create-function \
--function-name "$FUNCTION_NAME" \
--memory-size "$FUNCTION_MEMORY_SIZE" \
--timeout 120 \
--runtime "$RUNTIME" \
--package-type Zip \
--handler "serverless.benchmark.handler.Handler::handleRequest" \
--code S3Bucket="$BUCKET_NAME",S3Key="serverless-benchmark-$FN_TAG.zip" \
--role "$AWS_ROLE_ARN"
