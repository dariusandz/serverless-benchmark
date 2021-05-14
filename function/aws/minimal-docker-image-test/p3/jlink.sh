jlink --module-path ./build/libs:$JAVA_HOME/jmods \
   --add-modules  serverless.benchmark \
   --output ./dist \
   --launcher bootstrap=serverless.benchmark/serverless.benchmark.runtime.LambdaBootstrap \
   --compress 2 --no-header-files --no-man-pages --strip-debug

chmod +x bootstrap
chmod +x dist/bin/bootstrap
