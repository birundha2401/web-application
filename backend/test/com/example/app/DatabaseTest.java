package com.example.app;

public class DatabaseTest{
    public static void main(String[] args){
        System.out.println("--- Running DatabaseTest ---");
        testConfigLoading();
        testConnection();
        System.out.println("--- DatabaseTest Completed");
    }

    private static void testConfigLoading(){
        Database db = new Database("config/db.properties");
        if(db.getUrl() == null || db.getUrl().isEmpty()){
            throw new RuntimeException("FAILED: Database URL should not be empty!");
        }
        System.out.println("[PASS] Database configuration loaded successfully.");
    }

    private static void testConnection(){
        Database db = new Database("config/db.properties");
        boolean isConnected = db.checkConnection();
        if(!isConnected){
            System.out.println("[WARN] Database connection test failed. Ensure MySQL is running and config/db.properties credentials are valid.");
        }else{
            System.out.println("[PASS] Database connection verified successfully!");
        }
    }
}