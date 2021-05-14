# Builds native GraalVM image and packages to Docker image
FROM ghcr.io/graalvm/graalvm-ce:latest@sha256:6dcd95ceac521df2d3b44c2882b8f36ab786a6231c71dc3abd1f9d05b4d5de09 as build

RUN gu install native-image

WORKDIR /app

COPY src /app/src
COPY build.gradle /app/build.gradle
COPY gradle /app/gradle
COPY gradlew /app/gradlew

RUN ./gradlew build
RUN ./gradlew copyRuntimeDependencies

RUN native-image -jar /app/build/libs/app.jar \
    --verbose \
    -H:Name=bootstrap \
    --no-fallback \
    --enable-url-protocols=http

FROM debian:buster-slim

ENV LAMBDA_TASK_ROOT="/var/task"
ENV _HANDLER="serverless.benchmark.handler.Handler::handleRequest"

COPY bootstrap.sh /var/task/bootstrap
COPY --from=build /app/build/libs/app.jar /var/task/lib/
COPY --from=build /app/build/dependency/* /var/task/lib/
COPY --from=build /app/bootstrap /native-image/bootstrap

RUN ["chmod", "+x", "/var/task/bootstrap"]

WORKDIR $LAMBDA_TASK_ROOT

ENTRYPOINT ["/var/task/bootstrap"]
CMD ["serverless.benchmark.handler.Handler::handleRequest"]
