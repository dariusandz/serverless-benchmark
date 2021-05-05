package serverless.benchmark.handler;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import java.time.Duration;
import java.time.Instant;
import java.util.Map;

public class Handler implements RequestHandler<Map<String, String>, String> {

    static final int THREADS = Runtime.getRuntime().availableProcessors();

    private Boolean isCold = true;

    long artificialInitDuration;

    public Handler() {
        Instant initStart = Instant.now();
        matrix();
        Instant initEnd = Instant.now();
        artificialInitDuration = Duration.between(initStart, initEnd).toMillis();
    }

    @Override
    public String handleRequest(Map<String, String> input, Context context) {
        LambdaLogger logger = context.getLogger();

        if (isCold) {
            logger.log("Invoked a cold start function\n");
            logger.log("Available threads: " + THREADS + "\n");
            logger.log("Artificial initialization duration took: " + artificialInitDuration + " ms\n");
            isCold = false;
        }

        return "Hello Serverless";
    }

    static void matrix() {
        MatrixMultiplication m = new MatrixMultiplication();
        m.multiply();
    }
}