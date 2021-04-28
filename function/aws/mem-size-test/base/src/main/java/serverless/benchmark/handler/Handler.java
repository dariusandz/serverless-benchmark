package serverless.benchmark.handler;

import java.util.Arrays;
import java.util.Random;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import java.util.Map;
import java.util.logging.Logger;
import java.util.stream.IntStream;

public class Handler implements RequestHandler<Map<String, String>, String> {

    Logger logger = Logger.getLogger(Handler.class.getName());

    int arraySize = 100000000;

    int[] integerArray = new int[arraySize];

    int seed = 735482;

    Random random = new Random(seed);

    private Boolean isCold = true;

    public Handler() {
        initArray();
        doRandomCalculations();
    }

    @Override
    public String handleRequest(Map<String, String> input, Context context) {
        LambdaLogger logger = context.getLogger();

        if (isCold) {
            logger.log("Invoked a cold start function");
            isCold = false;
        }

        return "Hello Lambda!";
    }

    private void initArray() {
        logger.info("Initializing random array");
        IntStream.range(0, arraySize).forEach(i -> integerArray[i] = random.nextInt(arraySize) + 1);
    }

    private void doRandomCalculations() {
        logger.info("Doing random calculations");
        Arrays.stream(integerArray).forEach(i -> {
            int f = integerArray[Math.abs(i * seed) % arraySize];
            int s = integerArray[Math.abs(arraySize / i) % arraySize];
            int c = f * s;
        });
    }
}
