package serverless.benchmark.handler;

public class Handler {

    private Boolean isCold = true;

    public String handleRequest(Object input) {

        if (isCold) {
            System.out.println("Invoked a cold start function\n");
            isCold = false;
        }

        return "Hello Serverless";
    }
}
