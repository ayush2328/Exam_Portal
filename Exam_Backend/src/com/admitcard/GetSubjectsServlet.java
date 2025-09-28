package com.admitcard;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.WebServlet;
import java.io.*;
import org.json.JSONArray;
import org.json.JSONObject;

@WebServlet("/getSubjects")
public class GetSubjectsServlet extends HttpServlet {
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        // CORS headers - Production ke liye * use karo
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type");

        response.setContentType("application/json");
        JSONArray jsonArray = new JSONArray();

        String semParam = request.getParameter("sem");
        System.out.println("[DEBUG] Requested sem = " + semParam);

        int sem = 0;
        try {
            sem = Integer.parseInt(semParam);
        } catch (NumberFormatException e) {
            System.err.println("[ERROR] Invalid sem parameter: " + semParam);
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            PrintWriter out = response.getWriter();
            out.print("{\"error\":\"Invalid sem parameter\"}");
            return;
        }

        try {
            // MongoDB se subjects get karo
            JSONArray subjects = DBhelper.getSubjects(sem);
            
            // Format change karo frontend compatibility ke liye
            for (int i = 0; i < subjects.length(); i++) {
                JSONObject subject = subjects.getJSONObject(i);
                JSONObject obj = new JSONObject();
                obj.put("code", subject.getString("subject_code"));
                obj.put("name", subject.getString("subject_name"));
                jsonArray.put(obj);
            }

            System.out.println("[DEBUG] Number of subjects fetched = " + jsonArray.length());

        } catch (Exception e) {
            e.printStackTrace();
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            PrintWriter out = response.getWriter();
            out.print("{\"error\":\"Database error: " + e.getMessage() + "\"}");
            return;
        }

        PrintWriter out = response.getWriter();
        out.print(jsonArray.toString());
    }

    @Override
    protected void doOptions(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        // Preflight CORS support
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type");
        response.setStatus(HttpServletResponse.SC_OK);
    }
}