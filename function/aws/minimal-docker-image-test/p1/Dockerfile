# Builds unoptimized size Docker image
FROM amazoncorretto:11-alpine-jdk as build

WORKDIR /app

COPY src /app/src
COPY build.gradle /app/build.gradle
COPY gradle /app/gradle
COPY gradlew /app/gradlew

RUN ./gradlew build
RUN ./gradlew copyRuntimeDependencies

FROM amazoncorretto:11-alpine

# Custom runtime configuration
ENV LAMBDA_TASK_ROOT=/var/task
ENV _HANDLER=serverless.benchmark.handler.Handler::handleRequest

WORKDIR $LAMBDA_TASK_ROOT

COPY ./bootstrap.sh ${LAMBDA_TASK_ROOT}/bootstrap
COPY --from=build /app/build/dependency/* /var/task/lib/
COPY --from=build /app/build/libs/app.jar ${LAMBDA_TASK_ROOT}/lib/

RUN ["chmod", "+x", "/var/task/bootstrap"]

ENTRYPOINT ["/var/task/bootstrap"]
CMD ["serverless.benchmark.handler.Handler::handleRequest"]
