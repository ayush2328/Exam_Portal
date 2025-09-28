package com.admitcard;
import java.sql.*;
import java.util.Scanner;

public class AdmitCardGenerator {
    public static void main(String[] args) {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
           String url = "jdbc:mysql://localhost:3306/college_db?useSSL=false&allowPublicKeyRetrieval=true";

            String username = "root";
            String password = "Ayush@232829";

            Connection conn = DriverManager.getConnection(url, username, password);

            Scanner sc = new Scanner(System.in);
            System.out.print("Enter student Roll No: ");
            String rollNo = sc.nextLine();
            // PreparedStatement stmt = con.prepareStatement();

            String query = "SELECT * FROM StudentData WHERE reg_no = ?";
            PreparedStatement ps = conn.prepareStatement(query);
            ps.setString(1, rollNo);
            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                System.out.println("\n===== Admit Card =====");
                System.out.println("Name: " + rs.getString("student_name"));
                System.out.println("Roll No: " + rs.getString("reg_no"));
                System.out.println("Course: " + rs.getString("course"));
                System.out.println("Year: " + rs.getString("year"));
                System.out.println("Semester: " + rs.getString("sem"));
                System.out.println("Picture: " + rs.getString("pic"));

            } else {
                System.out.println("Student not found!");
            }

            conn.close();
            sc.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
