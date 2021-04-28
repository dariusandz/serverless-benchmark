#!/bin/bash
FUNCTION_NAME=$1

aws lambda delete-function \
--function-name "$FUNCTION_NAME"