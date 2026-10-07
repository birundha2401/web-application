package com.example.app;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public class Database {
    private String url;
    private String user;
    private String password;

    public Database(String configPath) {
        loadConfig(configPath);
    }

    private void loadConfig(String configPath) {
        Properties props = new Properties();
        try (InputStream input = new FileInputStream(configPath)) {
            props.load(input);
            this.url = props.getProperty("db.url");
            this.user = props.getProperty("db.user");
            this.password = props.getProperty("db.password");
        } catch (IOException e) {
            System.err.println("Error reading config file:" + configPath + "-" + e.getMessage());
        }
    }

    public Connection getConnection() throws SQLException {
        if (url == null || url.isEmpty()) {
            throw new SQLException("Database URL is not configured");
        }
        return DriverManager.getConnection(url, user, password);
    }

    public boolean checkConnection() {
        try (Connection conn = getConnection()) {
            return conn != null && !conn.isClosed();
        } catch (SQLException e) {
            System.err.println("Database connection check failed" + e.getMessage());
            return false;
        }
    }

    public String getUrl() {
        return url;
    }

    public String getUser() {
        return user;
    }
}