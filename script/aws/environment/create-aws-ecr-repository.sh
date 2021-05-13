#!/bin/bash
REPOSITORY_NAME=$1

aws ecr create-repository \
--repository-name "$REPOSITORY_NAME"