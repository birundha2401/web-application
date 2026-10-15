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

public class LoginHandler implements HttpHandler {
    private final UserRepository userRepo;

    public LoginHandler(Database db) {
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
            
            // Reusing our minimal regex parser
            String email = extractJsonValue(body, "email");
            String password = extractJsonValue(body, "password");

            if (email == null || password == null) {
                sendResponse(exchange, 400, "{\"error\":\"Missing email or password\"}");
                return;
            }

            User user = userRepo.getUserByEmail(email);
            
            // Use generic error for both missing user AND wrong password to prevent "account enumeration"
            if (user == null || !PasswordHash.verify(password, user.getPassword())) {
                sendResponse(exchange, 401, "{\"error\":\"Invalid email or password\"}");
                return;
            }

            // Authentication Successful
            sendResponse(exchange, 200, "{\"success\":true,\"message\":\"Login successful\"}");

        } catch (SQLException e) {
            System.err.println("Database error during login: " + e.getMessage());
            sendResponse(exchange, 500, "{\"error\":\"Internal Server Error\"}");
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