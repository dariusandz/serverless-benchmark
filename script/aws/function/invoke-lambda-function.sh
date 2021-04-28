#!/bin/bash
FUNCTION_NAME=$1

aws lambda invoke \
--function-name "$FUNCTION_NAME" log --log-type Tail