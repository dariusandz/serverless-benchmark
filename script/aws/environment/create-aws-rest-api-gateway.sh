#!/bin/bash
AWS_REGION=$1

GATEWAY_ID=$(aws apigateway create-rest-api \
--name 'LambdaBenchmarkGateway' \
--region "$AWS_REGION" | jq -r .id)

GATEWAY_ROOT_ID=$(aws apigateway get-resources \
--rest-api-id "$GATEWAY_ID" \
--region "$AWS_REGION" | jq -r .id)

AWS_GATEWAY_LAMBDA_RESOURCE_ID=$(aws apigateway create-resource \
--rest-api-id "$GATEWAY_ID" \
--region "$AWS_REGION" \
--parent-id "$GATEWAY_ROOT_ID" \
--path-part g1 | jq -r .id)

aws apigateway put-method \
--rest-api-id "$GATEWAY_ID" \
--region "$AWS_REGION" \
--resource-id "$AWS_GATEWAY_LAMBDA_RESOURCE_ID" \
--http-method POST \
--authorization-type "NONE"