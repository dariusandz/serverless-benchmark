#!/bin/sh
java -jar "./lib/aws-lambda-java-runtime-interface-client-1.0.0.jar" "serverless.benchmark.handler.Handler::handleRequest"