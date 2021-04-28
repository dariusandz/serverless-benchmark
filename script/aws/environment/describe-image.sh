#!/bin/bash
REPOSITORY_NAME=$1
IMAGE_TAG=$2

aws ecr describe-images \
--repository-name "$REPOSITORY_NAME" \
--image-ids imageTag="$IMAGE_TAG"