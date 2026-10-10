package com.example.app;

public class PasswordHashTest {
    public static void main(String[] args) {
        System.out.println("--- Running PasswordHashTest ---");
        testDifferentSalts();
        testVerifyCorrectPassword();
        testVerifyIncorrectPassword();
        System.out.println("--- PasswordHashTest Completed ---");
    }

    private static void testDifferentSalts() {
        String pass = "mysecretpassword";
        String hash1 = PasswordHash.hash(pass);
        String hash2 = PasswordHash.hash(pass);
        
        if (hash1.equals(hash2)) {
            throw new RuntimeException("FAILED: Hashes should be different due to random salts.");
        }
        System.out.println("[PASS] Identical passwords generate unique hashes (salting works).");
    }

    private static void testVerifyCorrectPassword() {
        String pass = "mysecretpassword";
        String hash = PasswordHash.hash(pass);
        
        if (!PasswordHash.verify(pass, hash)) {
            throw new RuntimeException("FAILED: Verification failed for the correct password.");
        }
        System.out.println("[PASS] Correct password verified successfully.");
    }

    private static void testVerifyIncorrectPassword() {
        String pass = "mysecretpassword";
        String hash = PasswordHash.hash(pass);
        
        if (PasswordHash.verify("wrongpassword", hash)) {
            throw new RuntimeException("FAILED: Verification succeeded for the wrong password.");
        }
        System.out.println("[PASS] Incorrect password correctly rejected.");
    }
}