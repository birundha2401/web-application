package com.example.app;

import org.mindrot.jbcrypt.BCrypt;

public class PasswordHash {
    
    // Generates a BCrypt hash with a work factor of 12
    public static String hash(String password) {
        return BCrypt.hashpw(password, BCrypt.gensalt(12));
    }

    // Verifies a plaintext password against a stored BCrypt hash
    public static boolean verify(String password, String storedHash) {
        try {
            return BCrypt.checkpw(password, storedHash);
        } catch (Exception e) {
            return false;
        }
    }
}