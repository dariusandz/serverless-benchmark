#!/bin/bash
FUNCTION_NAME=$1

aws lambda get-function \
--function-name "$FUNCTION_NAME"