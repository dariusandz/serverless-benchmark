FROM openjdk:11-jre-slim

# Custom runtime configuration
ENV LAMBDA_TASK_ROOT=/var/task

WORKDIR $LAMBDA_TASK_ROOT

COPY ./bootstrap.sh ${LAMBDA_TASK_ROOT}/bootstrap

COPY build/libs/* ${LAMBDA_TASK_ROOT}/lib/
COPY build/dependency/* ${LAMBDA_TASK_ROOT}/lib/

RUN ["chmod", "+x", "/var/task/bootstrap"]
