# Bundles jlinked runtime with Docker image
FROM maven:3.6.1-jdk-13-alpine as build

WORKDIR /app

COPY src src
COPY build.gradle build.gradle
COPY gradle gradle
COPY gradlew gradlew
COPY bootstrap bootstrap

RUN ./gradlew build
RUN ./gradlew copyRuntimeDependencies

RUN jlink --module-path ./build/libs:$JAVA_HOME/jmods \
       --add-modules serverless.benchmark \
       --output ./dist \
       --launcher bootstrap=serverless.benchmark/serverless.benchmark.runtime.LambdaBootstrap \
       --compress 2 --no-header-files --no-man-pages --strip-debug

FROM alpine:latest

# Custom runtime configuration
ENV LAMBDA_TASK_ROOT=/var/task
ENV _HANDLER=serverless.benchmark.handler.Handler::handleRequest

COPY --from=build /app/bootstrap ${LAMBDA_TASK_ROOT}/bootstrap
COPY --from=build /app/dist/ /var/task/dist/
COPY --from=build /app/build/dependency /var/task/lib/

RUN ["chmod", "+x", "/var/task/bootstrap"]
RUN ["chmod", "+x", "/var/task/dist/bin/bootstrap"]

WORKDIR $LAMBDA_TASK_ROOT

ENTRYPOINT ["/var/task/bootstrap"]
CMD ["serverless.benchmark.handler.Handler::handleRequest"]
