#!/bin/bash
FUNCTION_NAME=$1
AWS_ROLE_ARN_ID=$2
LAYER_NAME=$3

aws lambda update-function-configuration \
  --function-name "$FUNCTION_NAME" \
  --layers arn:aws:lambda:eu-west-1:"$AWS_ROLE_ARN_ID":layer:"$LAYER_NAME":1