package com.example.app;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Path;
import java.nio.file.Paths;

public class StaticFileHandler implements HttpHandler {
    private final String baseDir;

    public StaticFileHandler(String baseDir) {
        this.baseDir = baseDir;
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
            sendResponse(exchange, 405, "405 Method Not Allowed", "text/plain");
            return;
        }

        String requestPath = exchange.getRequestURI().getPath();
        if (requestPath.equals("/") || requestPath.isEmpty()) {
            requestPath = "/index.html";
        }

        Path basePath = Paths.get(baseDir).toAbsolutePath().normalize();
        Path targetPath = basePath.resolve(requestPath.substring(1)).normalize();

        // Prevent directory traversal attacks
        if (!targetPath.startsWith(basePath)) {
            sendResponse(exchange, 403, "403 Forbidden", "text/plain");
            return;
        }

        File file = targetPath.toFile();
        if (!file.exists() || file.isDirectory()) {
            sendResponse(exchange, 404, "404 Not Found", "text/plain");
            return;
        }

        String mimeType = getMimeType(file.getName());
        exchange.getResponseHeaders().set("Content-Type", mimeType);
        exchange.sendResponseHeaders(200, file.length());

        try (FileInputStream fis = new FileInputStream(file);
             OutputStream os = exchange.getResponseBody()) {
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                os.write(buffer, 0, bytesRead);
            }
        }
    }

    private void sendResponse(HttpExchange exchange, int statusCode, String responseText, String contentType) throws IOException {
        byte[] bytes = responseText.getBytes();
        exchange.getResponseHeaders().set("Content-Type", contentType);
        exchange.sendResponseHeaders(statusCode, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }

    private String getMimeType(String filename) {
        if (filename.endsWith(".html") || filename.endsWith(".htm")) return "text/html; charset=UTF-8";
        if (filename.endsWith(".css")) return "text/css; charset=UTF-8";
        if (filename.endsWith(".js")) return "application/javascript; charset=UTF-8";
        if (filename.endsWith(".json")) return "application/json; charset=UTF-8";
        if (filename.endsWith(".png")) return "image/png";
        if (filename.endsWith(".jpg") || filename.endsWith(".jpeg")) return "image/jpeg";
        if (filename.endsWith(".ico")) return "image/x-icon";
        return "application/octet-stream";
    }
}