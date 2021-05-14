package serverless.benchmark.runtime;

import serverless.benchmark.handler.Handler;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.MessageFormat;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class LambdaBootstrap {

    private static final String LAMBDA_VERSION_DATE = "2018-06-01";
    private static final String LAMBDA_RUNTIME_URL_TEMPLATE = "http://{0}/{1}/runtime/invocation/next";
    private static final String LAMBDA_INVOCATION_URL_TEMPLATE = "http://{0}/{1}/runtime/invocation/{2}/response";
    private static final String LAMBDA_INIT_ERROR_URL_TEMPLATE = "http://{0}/{1}/runtime/init/error";
    private static final String LAMBDA_ERROR_URL_TEMPLATE = "http://{0}/{1}/runtime/invocation/{2}/error";

    public static void main(String[] args) {

        String runtimeApi = getEnv("AWS_LAMBDA_RUNTIME_API");
        String taskRoot = getEnv("LAMBDA_TASK_ROOT");
        String handlerName = getEnv("_HANDLER");

        Handler handler = new Handler();


        String requestId;
        String runtimeUrl = MessageFormat.format(LAMBDA_RUNTIME_URL_TEMPLATE, runtimeApi, LAMBDA_VERSION_DATE);

        // Main event loop
        while (true) {

            // Get next Lambda Event
            SimpleHttpResponse event = get(runtimeUrl);
            requestId = getHeaderValue("Lambda-Runtime-Aws-Request-Id", event.getHeaders());

            try {
                // Invoke Handler Method
                String result = invoke(handler, event.getBody());

                // Post the results of Handler Invocation
                String invocationUrl = MessageFormat.format(LAMBDA_INVOCATION_URL_TEMPLATE, runtimeApi, LAMBDA_VERSION_DATE, requestId);
                post(invocationUrl, result);
            } catch (Exception e) {
                String initErrorUrl = MessageFormat.format(LAMBDA_ERROR_URL_TEMPLATE, runtimeApi, LAMBDA_VERSION_DATE, requestId);
                postError(initErrorUrl, "Invocation Error", "RuntimeError");
                e.printStackTrace();
            }
        }
    }

    private static final String ERROR_RESPONSE_TEMPLATE = "'{'" +
            "\"errorMessage\": \"{0}\"," +
            "\"errorType\": \"{1}\"" +
            "'}'";

    private static void postError(String errorUrl, String errMsg, String errType) {
        String error = MessageFormat.format(ERROR_RESPONSE_TEMPLATE, errMsg, errType);
        post(errorUrl, error);
    }

    private static String invoke(Handler handler, Object payload) {

        return handler.handleRequest(payload);
    }

    private static String getHeaderValue(String header, Map<String, List<String>> headers) {
        List<String> values = headers.get(header);

        // We don't expect any headers with multiple values, so for simplicity we'll just concat any that have more than one entry.
        return String.join(",", values);
    }

    private static String getEnv(String name) {
        return System.getenv(name);
    }

    private static SimpleHttpResponse get(String remoteUrl) {

        SimpleHttpResponse output = null;

        try {
            URL url = new URL(remoteUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            // Parse the HTTP Response
            output = readResponse(conn);
        } catch(IOException e) {
            System.out.println("GET: " + remoteUrl);
            e.printStackTrace();
        }

        return output;
    }

    private static SimpleHttpResponse post(String remoteUrl, String body) {
        SimpleHttpResponse output = null;

        try {
            URL url = new URL(remoteUrl);
            HttpURLConnection conn = (HttpURLConnection)url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            setBody(conn, body);
            conn.connect();

            // We can probably skip this for speed because we don't really care about the response
            output = readResponse(conn);
        }
        catch(IOException ioe) {
            System.out.println("POST: " + remoteUrl);
            ioe.printStackTrace();
        }

        return output;
    }

    private static SimpleHttpResponse readResponse(HttpURLConnection conn) throws IOException{

        // Map Response Headers
        HashMap<String, List<String>> headers = new HashMap<>();

        for(Map.Entry<String, List<String>> entry : conn.getHeaderFields().entrySet()) {
            headers.put(entry.getKey(), entry.getValue());
        }

        // Map Response Body
        BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
        StringBuilder result = new StringBuilder();

        String line;

        while ((line = rd.readLine()) != null) {
            result.append(line);
        }

        rd.close();

        return new SimpleHttpResponse(conn.getResponseCode(), headers, result.toString());
    }

    private static void setBody(HttpURLConnection conn, String body) throws IOException{
        OutputStream os = null;
        OutputStreamWriter osw = null;

        try {
            os = conn.getOutputStream();
            osw = new OutputStreamWriter(os, "UTF-8");

            osw.write(body);
            osw.flush();
        } finally {
            osw.close();
            os.close();
        }
    }
}

