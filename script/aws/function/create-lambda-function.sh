#!/bin/bash
FUNCTION_NAME=$1
FUNCTION_MEMORY_SIZE=$2
AWS_IMAGE_URI=$3
AWS_ROLE_ARN=$4

aws lambda create-function \
--function-name "$FUNCTION_NAME" \
--memory-size "$FUNCTION_MEMORY_SIZE" \
--package-type Image \
--code ImageUri="$AWS_IMAGE_URI" \
--role "$AWS_ROLE_ARN"
