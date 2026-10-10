package com.example.app;

import com.sun.net.httpserver.HttpServer;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.URL;
import java.sql.Connection;
import java.sql.Statement;

public class RegisterHandlerTest {
    private static final int TEST_PORT = 8090;

    public static void main(String[] args) throws Exception {
        System.out.println("--- Running RegisterHandlerTest ---");

        Database db = new Database("config/db.properties");
        
        // Setup: clear test data
        try (Connection conn = db.getConnection(); Statement stmt = conn.createStatement()) {
            stmt.execute("DELETE FROM users WHERE email LIKE 'api%@example.com'");
        }

        HttpServer server = HttpServer.create(new InetSocketAddress(TEST_PORT), 0);
        server.createContext("/api/register", new RegisterHandler(db));
        server.start();

        try {
            testValidRegistration();
            testDuplicateRegistration();
            testMissingFields();
            System.out.println("--- RegisterHandlerTest Completed ---");
        } finally {
            server.stop(0);
        }
    }

    private static void testValidRegistration() throws Exception {
        int code = sendPost("{\"name\":\"API Test\",\"phone\":\"123\",\"email\":\"api1@example.com\",\"password\":\"pass\"}");
        if (code != 201) throw new RuntimeException("FAILED: Expected 201 Created, got " + code);
        System.out.println("[PASS] Valid registration returned 201.");
    }

    private static void testDuplicateRegistration() throws Exception {
        sendPost("{\"name\":\"API Test\",\"phone\":\"123\",\"email\":\"api2@example.com\",\"password\":\"pass\"}");
        int code = sendPost("{\"name\":\"API Test\",\"phone\":\"123\",\"email\":\"api2@example.com\",\"password\":\"pass\"}");
        if (code != 409) throw new RuntimeException("FAILED: Expected 409 Conflict, got " + code);
        System.out.println("[PASS] Duplicate email correctly returned 409.");
    }

    private static void testMissingFields() throws Exception {
        int code = sendPost("{\"name\":\"API Test\",\"phone\":\"123\"}");
        if (code != 400) throw new RuntimeException("FAILED: Expected 400 Bad Request, got " + code);
        System.out.println("[PASS] Missing fields correctly returned 400.");
    }

    private static int sendPost(String jsonPayload) throws Exception {
        URL url = new URL("http://localhost:" + TEST_PORT + "/api/register");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        try (OutputStream os = conn.getOutputStream()) {
            os.write(jsonPayload.getBytes());
        }
        return conn.getResponseCode();
    }
}