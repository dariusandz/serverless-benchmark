package serverless.benchmark.handler;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import java.time.Duration;
import java.time.Instant;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class Handler implements RequestHandler<Map<String, String>, String> {

    private Boolean isCold = true;

    long artificialInitDuration;

    public Handler() {
//        Instant initStart = Instant.now();
//        primeNumbersBruteForce(100000);
//        Instant initEnd = Instant.now();
//        artificialInitDuration = Duration.between(initStart, initEnd).toMillis();
    }

    @Override
    public String handleRequest(Map<String, String> input, Context context) {
        LambdaLogger logger = context.getLogger();

        if (isCold) {
            logger.log("Invoked a cold start function\n");
            logger.log("Artificial initialization duration took: " + artificialInitDuration + " ms\n");
            isCold = false;
        }

        return "Hello Serverless";
    }

    public static List<Integer> primeNumbersBruteForce(int n) {
        List<Integer> primeNumbers = new LinkedList<>();
        for (int i = 2; i <= n; i++) {
            if (isPrimeBruteForce(i)) {
                primeNumbers.add(i);
            }
        }
        return primeNumbers;
    }
    public static boolean isPrimeBruteForce(int number) {
        for (int i = 2; i < number; i++) {
            if (number % i == 0) {
                return false;
            }
        }
        return true;
    }
}
