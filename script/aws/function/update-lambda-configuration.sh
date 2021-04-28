#!/bin/bash
FUNCTION_NAME=$1

aws lambda update-function-configuration \
--function-name "$FUNCTION_NAME" \
--image-config \
'{
    "EntryPoint": ["/var/task/bootstrap"],
    "Command": ["serverless.benchmark.handler.Handler::handleRequest"],
    "WorkingDirectory": "/var/task"
}'
