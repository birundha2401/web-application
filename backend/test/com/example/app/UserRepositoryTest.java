package com.example.app;

import java.sql.Connection;
import java.sql.Statement;

public class UserRepositoryTest {
    public static void main(String[] args) throws Exception {
        System.out.println("--- Running UserRepositoryTest ---");
        
        Database db = new Database("config/db.properties");
        UserRepository repo = new UserRepository(db);
        
        // Setup: clear test data
        try (Connection conn = db.getConnection();
             Statement stmt = conn.createStatement()) {
            stmt.execute("DELETE FROM users WHERE email LIKE 'test%@example.com'");
        }
        
        testSaveValidUser(repo);
        testDuplicateEmailThrowsException(repo);
        
        testGetUserByEmail(repo);
        testUserNotFound(repo);
        
        System.out.println("--- UserRepositoryTest Completed ---");
    }

    private static void testSaveValidUser(UserRepository repo) throws Exception {
        User user = new User("Test Name", "1234567890", "test1@example.com", "plainpassword");
        boolean success = repo.saveUser(user);
        if (!success) throw new RuntimeException("FAILED: Expected user to be saved successfully.");
        System.out.println("[PASS] Valid user saved successfully.");
    }

    private static void testDuplicateEmailThrowsException(UserRepository repo) {
        User user1 = new User("Test 2", "0987654321", "test2@example.com", "pass1");
        User user2 = new User("Test 3", "1111111111", "test2@example.com", "pass2");
        
        try {
            repo.saveUser(user1);
            repo.saveUser(user2);
            throw new RuntimeException("FAILED: Expected SQLException for duplicate email.");
        } catch (Exception e) {
            if (e.getMessage().contains("Duplicate entry")) {
                System.out.println("[PASS] Duplicate email correctly rejected by database constraint.");
            } else {
                throw new RuntimeException("FAILED: Unexpected exception: " + e.getMessage());
            }
        }
    }

    private static void testGetUserByEmail(UserRepository repo) throws Exception {
        // Notice it uses getUserByEmail, not testGetUserByEmail
        User user = repo.getUserByEmail("test1@example.com");
        if (user == null || !user.getName().equals("Test Name")) {
            throw new RuntimeException("FAILED: Expected to retrieve existing user 'Test Name'.");
        }
        System.out.println("[PASS] Retrieved existing user by email.");
    }

    private static void testUserNotFound(UserRepository repo) throws Exception {
        User user = repo.getUserByEmail("doesnotexist@example.com");
        if (user != null) {
            throw new RuntimeException("FAILED: Expected null for non-existent user.");
        }
        System.out.println("[PASS] Correctly returned null for missing user.");
    }
}