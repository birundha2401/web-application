package com.example.app;

import com.sun.net.httpserver.HttpServer;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.URL;

public class HealthHandlerTest{
    private static final int TEST_PORT = 8089;

    public static void main(String[] args) throws Exception{
        System.out.println("--- Running HealthHandlerTest ---");

        Database db = new Database("config/db.properties");
        HttpServer server = HttpServer.create(new InetSocketAddress(TEST_PORT),0);
        server.createContext("/api/health",new HealthHandler(db));
        server.start();

        try{
            testHealthCheckReturnsSuccess();
            testNonGetMethodReturns405();
            System.out.println("--- HealthHandlerTest Completes ---");
        }
        finally{
            server.stop(0);
        }
    }

     private static void testHealthCheckReturnsSuccess() throws Exception {
        URL url = new URL("http://localhost:" + TEST_PORT + "/api/health");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        int responseCode = conn.getResponseCode();
        String contentType = conn.getHeaderField("Content-Type");
        InputStream in = (responseCode == 200) ? conn.getInputStream() : conn.getErrorStream();
        String body = new String(in.readAllBytes());
        if (responseCode != 200) {
            throw new RuntimeException("FAILED: Expected HTTP 200, got " + responseCode);
        }
        if (contentType == null || !contentType.contains("application/json")) {
            throw new RuntimeException("FAILED: Expected Content-Type application/json, got " + contentType);
        }
        if (!body.contains("\"status\":\"UP\"")) {
            throw new RuntimeException("FAILED: Response body missing status:UP. Got: " + body);
        }
        System.out.println("[PASS] Health endpoint returned HTTP 200 OK with valid JSON: " + body);
    }
    private static void testNonGetMethodReturns405() throws Exception {
        URL url = new URL("http://localhost:" + TEST_PORT + "/api/health");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        int responseCode = conn.getResponseCode();
        if (responseCode != 405) {
            throw new RuntimeException("FAILED: Expected HTTP 405 Method Not Allowed, got " + responseCode);
        }
        System.out.println("[PASS] Non-GET method correctly returned HTTP 405.");
    }
}