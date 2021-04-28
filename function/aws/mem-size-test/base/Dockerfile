FROM public.ecr.aws/lambda/java:11

ENV AWS_LAMBDA_FUNCTION_MEMORY_SIZE=256

COPY build/libs/* ${LAMBDA_TASK_ROOT}/lib/
COPY build/dependency/* ${LAMBDA_TASK_ROOT}/lib/

CMD [ "serverless.benchmark.handler.Handler::handleRequest" ]
