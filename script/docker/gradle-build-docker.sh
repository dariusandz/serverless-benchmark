#!/bin/bash

PATH_TO_ROOT_DIR=$1
AWS_DOCKER_REPO=$2

export $(cat ".env" | xargs)

cd "$PATH_TO_ROOT_DIR" || exit
./gradlew buildDocker -Pdocker-repo="$AWS_DOCKER_REPO"

