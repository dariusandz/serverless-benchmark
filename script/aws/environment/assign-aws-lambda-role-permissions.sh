#!/bin/bash

aws iam attach-role-policy \
--role-name lambda-benchmark \
--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole