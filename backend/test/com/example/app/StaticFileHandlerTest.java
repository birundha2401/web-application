package com.example.app;

import com.sun.net.httpserver.HttpServer;
import java.io.File;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.URL;
import java.nio.file.Files;

public class StaticFileHandlerTest {
    private static final int TEST_PORT = 8088;

    public static void main(String[] args) throws Exception {
        System.out.println("--- Running StaticFileHandlerTest ---");

        File testDir = new File("frontend");
        if (!testDir.exists()) testDir.mkdirs();
        File testFile = new File("frontend/index.html");
        if (!testFile.exists()) {
            Files.writeString(testFile.toPath(), "<html>Test Landing Page</html>");
        }

        HttpServer server = HttpServer.create(new InetSocketAddress(TEST_PORT), 0);
        server.createContext("/", new StaticFileHandler("frontend"));
        server.start();

        try {
            testServesIndexHtml();
            testReturns404ForMissingFile();
            System.out.println("--- StaticFileHandlerTest Completed ---");
        } finally {
            server.stop(0);
        }
    }

    private static void testServesIndexHtml() throws Exception {
        URL url = new URL("http://localhost:" + TEST_PORT + "/");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        int status = conn.getResponseCode();
        String contentType = conn.getHeaderField("Content-Type");

        if (status != 200) {
            throw new RuntimeException("FAILED: Expected HTTP 200, got " + status);
        }
        if (contentType == null || !contentType.contains("text/html")) {
            throw new RuntimeException("FAILED: Expected Content-Type text/html, got " + contentType);
        }

        System.out.println("[PASS] Root URL correctly serves index.html with HTTP 200.");
    }

    private static void testReturns404ForMissingFile() throws Exception {
        URL url = new URL("http://localhost:" + TEST_PORT + "/nonexistent-file.css");
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        int status = conn.getResponseCode();
        if (status != 404) {
            throw new RuntimeException("FAILED: Expected HTTP 404, got " + status);
        }

        System.out.println("[PASS] Missing file request correctly returns HTTP 404.");
    }
}