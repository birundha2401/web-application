package com.example.app;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;

public class Server {
    private static final int PORT = 8080;

    public static void main(String[] args) {
        try {
            Database db = new Database("config/db.properties");
            HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);

            // Register Health Check API Endpoint
            server.createContext("/api/health", new HealthHandler(db));

   
            // Register Registration API Endpoint
            server.createContext("/api/register", new RegisterHandler(db));

            // Register Login API Endpoint
            server.createContext("/api/login", new LoginHandler(db));

            // Register Static File Handler for Frontend
            server.createContext("/", new StaticFileHandler("frontend"));

            server.setExecutor(null);

            System.out.println("==================================================");
            System.out.println(" Server started at http://localhost:" + PORT);
            System.out.println(" Health API:  http://localhost:" + PORT + "/api/health");
            System.out.println(" Landing Page:http://localhost:" + PORT + "/");
            System.out.println("==================================================");

            server.start();

        } catch (IOException e) {
            System.err.println("Failed to start server: " + e.getMessage());
        }
    }
}