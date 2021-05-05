package serverless.benchmark.handler;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import java.io.File;
import java.io.IOException;
import java.util.Map;

public class Handler implements RequestHandler<Map<String, String>, String> {

    private Boolean isCold = true;

    @Override
    public String handleRequest(Map<String, String> input, Context context) {
        LambdaLogger logger = context.getLogger();

        if (writeToFile(logger) && isCold) {
            logger.log("Invoked a cold start function\n");
            isCold = false;
        }

        return "Hello Serverless";
    }

    private boolean writeToFile(LambdaLogger logger) {
        String tempDir = "/tmp/";
        String fileName = "invocation.txt";
        File f = new File(tempDir + fileName);
        try {
            if (f.createNewFile()) {
                logger.log("Successfully wrote to file\n");
                return true;
            } else {
                logger.log("File already exists - function context is reused\n");
                return false;
            }
        } catch (IOException e) {
            logger.log("Could not write to file\n");
            logger.log(e.getMessage());
            return false;
        }
    }
}
