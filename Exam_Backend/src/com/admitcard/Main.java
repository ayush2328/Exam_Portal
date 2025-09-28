package com.admitcard;
import java.sql.Connection;
import java.sql.DriverManager;

public class Main {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/exam_portal";
        String user = "root";
        String password = "Ayush@232829";  // <-- agar password hai to yahan dalna, nahi hai to blank

        try {
            Connection conn = DriverManager.getConnection(url, user, password);
            System.out.println("✅ Database connected successfully!");
            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
