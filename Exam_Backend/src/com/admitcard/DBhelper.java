package com.admitcard;

import com.mongodb.client.*;
import org.bson.Document;
import org.json.JSONArray;
import org.json.JSONObject;

public class DBhelper {
    private static MongoClient mongoClient;
    private static MongoDatabase database;
    
    // Static block - automatically connect when class loads
    static {
        connect();
    }
    
    public static void connect() {
        try {
            // Local MongoDB - Production mein environment variable use kareinge
            String mongoUri = System.getenv("MONGODB_URI");
            if (mongoUri == null) {
                mongoUri = "mongodb://localhost:27017";
            }
            
            mongoClient = MongoClients.create(mongoUri);
            database = mongoClient.getDatabase("exam_portal");
            System.out.println("✅ Connected to MongoDB successfully");
        } catch (Exception e) {
            System.err.println("❌ MongoDB connection failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    // Get subjects by semester (GetSubjectsServlet ke liye)
    public static JSONArray getSubjects(int semester) {
        JSONArray subjects = new JSONArray();
        try {
            MongoCollection<Document> collection = database.getCollection("subjects");
            
            // Convert semester to integer kyunki data integer format mein hai
            Document query = new Document("sem", semester);
            FindIterable<Document> results = collection.find(query);
            
            for (Document doc : results) {
                JSONObject subject = new JSONObject();
                subject.put("subject_id", doc.getInteger("subject_id"));
                subject.put("subject_name", doc.getString("subject_name"));
                subject.put("subject_code", doc.getString("subject_code"));
                subject.put("sem", doc.getInteger("sem"));
                subjects.put(subject);
            }
            
            System.out.println("📚 Found " + subjects.length() + " subjects for semester " + semester);
        } catch (Exception e) {
            System.err.println("❌ Error fetching subjects: " + e.getMessage());
            e.printStackTrace();
        }
        return subjects;
    }
    
    // Add exam session (AddExamSessionServlet ke liye)
    public static boolean addExamSession(String subjectCode, String examDate, 
                                       String examTime, int semester) {
        try {
            MongoCollection<Document> collection = database.getCollection("exams");
            
            Document exam = new Document()
                .append("subject_code", subjectCode)
                .append("exam_date", examDate)
                .append("exam_time", examTime)
                .append("semester", semester)
                .append("created_at", new java.util.Date());
                
            collection.insertOne(exam);
            System.out.println("✅ Exam session added successfully: " + subjectCode);
            return true;
        } catch (Exception e) {
            System.err.println("❌ Error adding exam session: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
    
    // Get students for admit card (AdmitCardGenerator ke liye)
    public static JSONArray getStudents(String semester, String branch) {
        JSONArray students = new JSONArray();
        try {
            MongoCollection<Document> collection = database.getCollection("students");
            
            Document query = new Document("sem", semester).append("branch", branch);
            FindIterable<Document> results = collection.find(query);
            
            for (Document doc : results) {
                JSONObject student = new JSONObject();
                student.put("student_name", doc.getString("student_name"));
                student.put("reg_no", doc.getString("reg_no"));
                student.put("course", doc.getString("course"));
                student.put("branch", doc.getString("branch"));
                student.put("year", doc.getString("year"));
                student.put("sem", doc.getString("sem"));
                student.put("pic", doc.getString("pic"));
                student.put("contact_no", doc.getString("contact_no"));
                student.put("email_id", doc.getString("email_id"));
                students.put(student);
            }
            
            System.out.println("👨‍🎓 Found " + students.length() + " students for " + semester + ", " + branch);
        } catch (Exception e) {
            System.err.println("❌ Error fetching students: " + e.getMessage());
            e.printStackTrace();
        }
        return students;
    }
    
    // Get student by registration number
    public static JSONObject getStudentByRegNo(String regNo) {
        try {
            MongoCollection<Document> collection = database.getCollection("students");
            
            Document query = new Document("reg_no", regNo);
            Document studentDoc = collection.find(query).first();
            
            if (studentDoc != null) {
                JSONObject student = new JSONObject();
                student.put("student_name", studentDoc.getString("student_name"));
                student.put("reg_no", studentDoc.getString("reg_no"));
                student.put("course", studentDoc.getString("course"));
                student.put("branch", studentDoc.getString("branch"));
                student.put("year", studentDoc.getString("year"));
                student.put("sem", studentDoc.getString("sem"));
                student.put("pic", studentDoc.getString("pic"));
                student.put("contact_no", studentDoc.getString("contact_no"));
                student.put("email_id", studentDoc.getString("email_id"));
                return student;
            }
        } catch (Exception e) {
            System.err.println("❌ Error fetching student: " + e.getMessage());
            e.printStackTrace();
        }
        return null;
    }
    
    // Close connection (optional - MongoDB driver handles connection pooling)
    public static void close() {
        if (mongoClient != null) {
            mongoClient.close();
            System.out.println("🔌 MongoDB connection closed");
        }
    }
}