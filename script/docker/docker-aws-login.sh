#!/bin/bash
AWS_REGION=$1
AWS_ECR_URI=$2

aws ecr get-login-password \
--region "$AWS_REGION" | docker login \
  --username AWS \
  --password-stdin "$AWS_ECR_URI"