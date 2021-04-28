package serverless.benchmark.handler;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import java.util.Map;

public class Handler implements RequestHandler<Map<String, String>, String> {

    private Boolean isCold = true;

    @Override
    public String handleRequest(Map<String, String> input, Context context) {
        LambdaLogger logger = context.getLogger();

        if (isCold) {
            logger.log("Invoked a cold start function");
            isCold = false;
        }

        return "Hello Serverless";
    }
}
