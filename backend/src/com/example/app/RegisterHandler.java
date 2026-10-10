package com.example.app;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.sql.SQLException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RegisterHandler implements HttpHandler {
    private final UserRepository userRepo;

    public RegisterHandler(Database db) {
        this.userRepo = new UserRepository(db);
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
            sendResponse(exchange, 405, "{\"error\":\"Method Not Allowed\"}");
            return;
        }

        try (InputStream is = exchange.getRequestBody()) {
            String body = new String(is.readAllBytes(), StandardCharsets.UTF_8);
            
            // Minimal regex-based JSON extraction to avoid external library dependencies
            String name = extractJsonValue(body, "name");
            String phone = extractJsonValue(body, "phone");
            String email = extractJsonValue(body, "email");
            String password = extractJsonValue(body, "password");

            if (name == null || phone == null || email == null || password == null) {
                sendResponse(exchange, 400, "{\"error\":\"Missing required fields\"}");
                return;
            }

            User newUser = new User(name, phone, email, password);
            
            try {
                userRepo.saveUser(newUser);
                sendResponse(exchange, 201, "{\"message\":\"User registered successfully\"}");
            } catch (SQLException e) {
                if (e.getMessage().contains("Duplicate entry")) {
                    sendResponse(exchange, 409, "{\"error\":\"Email already exists\"}");
                } else {
                    System.err.println("Database error: " + e.getMessage());
                    sendResponse(exchange, 500, "{\"error\":\"Internal Server Error\"}");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
            sendResponse(exchange, 500, "{\"error\":\"Internal Server Error\"}");
        }
    }

    private String extractJsonValue(String json, String key) {
        String pattern = "\"" + key + "\"\\s*:\\s*\"([^\"]+)\"";
        Matcher m = Pattern.compile(pattern).matcher(json);
        return m.find() ? m.group(1) : null;
    }

    private void sendResponse(HttpExchange exchange, int statusCode, String responseText) throws IOException {
        byte[] bytes = responseText.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.sendResponseHeaders(statusCode, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }
}