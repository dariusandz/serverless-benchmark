#!/bin/bash
LAYER_NAME=$1
LAYER_PATH=$2

aws lambda publish-layer-version \
  --layer-name "$LAYER_NAME" \
  --zip-file fileb://"$LAYER_PATH"/build/distributions/runtime-layer.zip