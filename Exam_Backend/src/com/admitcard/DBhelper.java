package com.admitcard;

import java.sql.*;

public class DBhelper {
    private static final String URL = "jdbc:mysql://localhost:3306/examdb";
    private static final String USER = "root";
    private static final String PASSWORD = "Ayush@232829";
    
    public static Connection getConnection() throws SQLException {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            return DriverManager.getConnection(URL, USER, PASSWORD);
        } catch (ClassNotFoundException e) {
            throw new SQLException("MySQL JDBC Driver not found", e);
        }
    }
}