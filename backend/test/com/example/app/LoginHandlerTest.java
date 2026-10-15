package com.example.app;

import com.sun.net.httpserver.HttpServer;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.URL;
import java.sql.Connection;
import java.sql.Statement;

public class LoginHandlerTest {
    private static final int TEST_PORT = 8091;

    public static void main(String[] args) throws Exception {
        System.out.println("--- Running LoginHandlerTest ---");

        Database db = new Database("config/db.properties");
        UserRepository repo = new UserRepository(db);

        // Setup test user
        try (Connection conn = db.getConnection(); Statement stmt = conn.createStatement()) {
            stmt.execute("DELETE FROM users WHERE email = 'loginapi@example.com'");
        }
        repo.saveUser(new User("Login Test", "123", "loginapi@example.com", "correctpassword"));

        HttpServer server = HttpServer.create(new InetSocketAddress(TEST_PORT), 0);
        server.createContext("/api/login", new LoginHandler(db));
        server.start();

        try {
            testValidLogin();
            testInvalidPassword();
            testNonExistentUser();
            System.out.println("--- LoginHandlerTest Completed ---");
        } finally {
            server.stop(0);
        }
    }

    private static void testValidLogin() throws Exception {
        int code = sendPost("{\"email\":\"loginapi@example.com\",\"password\":\"correctpassword\"}");
        if (code != 200) throw new RuntimeException("FAILED: Expected 200 OK, got " + code);
        System.out.println("[PASS] Valid credentials returned 200 OK.");
    }

    private static void testInvalidPassword() throws Exception {
        int code = sendPost("{\"email\":\"loginapi@example.com\",\"password\":\"wrongpassword\"}");
        if (code != 401) throw new RuntimeException("FAILED: Expected 401 Unauthorized, got " + code);
        System.out.println("[PASS] Invalid password returned 401 Unauthorized.");
    }

    private static void testNonExistentUser() throws Exception {
        int code = sendPost("{\"email\":\"nobody@example.com\",\"password\":\"somepassword\"}");
        if (code != 401) throw new RuntimeException("FAILED: Expected 401 Unauthorized, got " + code);
        System.out.println("[PASS] Non-existent user returned 401 Unauthorized.");
    }

    private static int sendPost(String jsonPayload) throws Exception {
        URL url = new URL("http://localhost:" + TEST_PORT + "/api/login");
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