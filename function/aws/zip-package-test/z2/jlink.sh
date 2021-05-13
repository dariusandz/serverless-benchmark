gradle build

jlink --module-path build/libs:/Users/darius/.sdkman/candidates/java/amazon-corretto-11.0.11.9.1-linux-x64/jmods \
   --add-modules  serverless.benchmark \
   --output runtime-layer/dist \
   --launcher bootstrap=serverless.benchmark/serverless.benchmark.runtime.LambdaBootstrap \
   --compress 2 --no-header-files --no-man-pages --strip-debug

cp bootstrap runtime-layer/

chmod +x runtime-layer/bootstrap
chmod +x runtime-layer/dist/bin/bootstrap

cd runtime-layer ; zip -r ../build/distributions/serverless-benchmark.zip * ; cd ..