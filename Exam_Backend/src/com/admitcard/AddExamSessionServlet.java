package com.admitcard;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.WebServlet;
import java.io.*;
import java.sql.*;
import org.json.JSONObject;

@WebServlet("/addExamSession")
public class AddExamSessionServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        // CORS headers
        response.setHeader("Access-Control-Allow-Origin", "http://localhost:3000");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type");

        response.setContentType("application/json");
        PrintWriter out = response.getWriter();

        try {
            // Get parameters from request
            String subjectCode = request.getParameter("subjectCode");
            String examDate = request.getParameter("examDate");
            String examTime = request.getParameter("examTime");
            String semester = request.getParameter("semester");

            // Validate parameters
            if (subjectCode == null || examDate == null || examTime == null || semester == null) {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                out.print("{\"error\":\"Missing parameters\"}");
                return;
            }

            // Insert into database
            try (Connection conn = DBhelper.getConnection()) {
                String sql = "INSERT INTO ExamSessions (subject_code, exam_date, exam_time, semester) VALUES (?, ?, ?, ?)";
                PreparedStatement ps = conn.prepareStatement(sql);
                ps.setString(1, subjectCode);
                ps.setString(2, examDate);
                ps.setString(3, examTime);
                ps.setInt(4, Integer.parseInt(semester));

                int rowsAffected = ps.executeUpdate();

                if (rowsAffected > 0) {
                    out.print("{\"success\":\"Exam session added successfully\"}");
                } else {
                    response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
                    out.print("{\"error\":\"Failed to add exam session\"}");
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            out.print("{\"error\":\"Database error: " + e.getMessage() + "\"}");
        }
    }

    @Override
    protected void doOptions(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        // Preflight CORS support
        response.setHeader("Access-Control-Allow-Origin", "http://localhost:3000");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type");
        response.setStatus(HttpServletResponse.SC_OK);
    }
}