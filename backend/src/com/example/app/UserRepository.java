package com.example.app;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class UserRepository {
    private final Database db;

    public UserRepository(Database db) {
        this.db = db;
    }

    public boolean saveUser(User user) throws SQLException {
        String sql = "INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)";
        try (Connection conn = db.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getPhone());
            stmt.setString(3, user.getEmail());
            stmt.setString(4, PasswordHash.hash(user.getPassword()));
            
            return stmt.executeUpdate() > 0;
        }
    }
}