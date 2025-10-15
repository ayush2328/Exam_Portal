from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pymongo import MongoClient
from bson import ObjectId
import os
import json

app = FastAPI(title="Exam Portal API", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
try:
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
    client = MongoClient(MONGODB_URL)
    db = client["exam_portal"]
    
    # Collections
    subjects_collection = db["subjects"]
    exam_sessions_collection = db["exam_sessions"]
    students_collection = db["students"]
    
    MONGO_AVAILABLE = True
    print("✅ MongoDB connected successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    MONGO_AVAILABLE = False

def convert_objectid(doc):
    """Convert ObjectId to string in MongoDB documents"""
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

@app.get("/")
async def root():
    return {"message": "Exam Portal Backend API", "status": "running", "mongo_available": MONGO_AVAILABLE}

@app.get("/subjects/")
async def get_subjects(sem: int):
    """Get subjects by semester"""
    if not MONGO_AVAILABLE:
        return {"error": "MongoDB not available", "subjects": []}
    
    try:
        # Use "sem" field to match your MongoDB data
        subjects = list(subjects_collection.find({"sem": sem}))
        subjects = [convert_objectid(subject) for subject in subjects]
        return {"subjects": subjects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching subjects: {str(e)}")

@app.post("/exam-sessions/")
async def add_exam_session(subject_code: str, exam_date: str, exam_time: str, sem: int):
    """Add new exam session"""
    if not MONGO_AVAILABLE:
        raise HTTPException(status_code=500, detail="MongoDB not available")
    
    try:
        # Use "sem" field to match your MongoDB data
        exam_data = {
            "subject_code": subject_code,
            "exam_date": exam_date,
            "exam_time": exam_time,
            "sem": sem
        }
        result = exam_sessions_collection.insert_one(exam_data)
        return {"message": "Exam session added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding exam session: {str(e)}")

@app.get("/exam-sessions/")
async def get_exam_sessions(sem: int = None):
    """Get all exam sessions, optionally filtered by semester"""
    if not MONGO_AVAILABLE:
        return {"error": "MongoDB not available", "sessions": []}
    
    try:
        # Use "sem" field to match your MongoDB data
        query = {"sem": sem} if sem is not None else {}
        sessions = list(exam_sessions_collection.find(query))
        sessions = [convert_objectid(session) for session in sessions]
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching exam sessions: {str(e)}")

@app.get("/students/")
async def get_students(sem: int = None):
    """Get students, optionally filtered by semester"""
    if not MONGO_AVAILABLE:
        return {"error": "MongoDB not available", "students": []}
    
    try:
        # Filter by semester if provided
        if sem is not None:
            semester_text_map = {
                1: "1st Semester",
                2: "2nd Semester",
                3: "3rd Semester",
                4: "4th Semester",
                5: "5th Semester",
                6: "6th Semester",
                7: "7th Semester",
                8: "8th Semester"
            }
            semester_text = semester_text_map.get(sem, f"{sem}th Semester")
            query = {"sem": semester_text}
        else:
            query = {}
        
        students = list(students_collection.find(query))
        
        for student in students:
            # Convert _id to string
            student["_id"] = str(student["_id"])
            
            # Public URL for frontend display
            student["image_url"] = f"http://localhost:8000/static/student_images/{student.get('pic', '')}"
            
            # Full local path for PDF generator
            student["image_path"] = os.path.join("static", "student_images", student.get("pic", "default_student_photo.jpg"))
        
        return {"students": students}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")



@app.get("/students-by-exam/{exam_session_id}")
async def get_students_by_exam_session(exam_session_id: str):
    """Get all students for a specific exam session"""
    if not MONGO_AVAILABLE:
        return {"error": "MongoDB not available", "students": []}
    
    try:
        print(f"🔍 Looking for exam session: {exam_session_id}")
        
        # Get exam session details
        exam_session = exam_sessions_collection.find_one({"_id": ObjectId(exam_session_id)})
        if not exam_session:
            raise HTTPException(status_code=404, detail="Exam session not found")
        
        print(f"✅ Found exam session: {exam_session}")
        
        exam_semester = exam_session.get("sem", "")
        print(f"🔍 Looking for students in semester: {exam_semester}")
        
        # Convert numeric semester to text format (e.g., 3 → "3rd Semester")
        semester_text_map = {
            1: "1st Semester",
            2: "2nd Semester", 
            3: "3rd Semester",
            4: "4th Semester",
            5: "5th Semester",
            6: "6th Semester",
            7: "7th Semester",
            8: "8th Semester"
        }
        
        semester_text = semester_text_map.get(exam_semester, f"{exam_semester}th Semester")
        print(f"🔄 Converted semester {exam_semester} → '{semester_text}'")
        
        # Get all students for that semester using text format
        students_query = {"sem": semester_text}
        students = list(students_collection.find(students_query))
        
        print(f"📊 Found {len(students)} students with query: {students_query}")
        
        students = [convert_objectid(student) for student in students]
        
        # Debug: Show first student structure if available
        if students:
            print(f"📋 Sample student structure: {students[0]}")
        
        return {
            "exam_session": convert_objectid(exam_session),
            "students": students
        }
    except Exception as e:
        print(f"❌ Error in get_students_by_exam_session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")

@app.get("/generate-admit-card/{student_id}")
async def generate_admit_card_pdf(student_id: str):
    """Generate admit card PDF"""
    if not MONGO_AVAILABLE:
        raise HTTPException(status_code=500, detail="MongoDB not available")
    
    try:
        print(f"🔍 Looking for student with ID: {student_id}")
        
        # Get student data
        student = students_collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        student_name = student.get('student_name', 'Unknown')
        student_semester = student.get("sem", "")
        print(f"✅ Found student: {student_name}")
        
        # Get ALL exam sessions for this semester
        student_semester_text = student_semester
        if isinstance(student_semester, str) and "Semester" in student_semester:
            semester_num = student_semester.replace("Semester", "").strip()
            if semester_num == "3rd":
                student_semester_num = 3
            else:
                try:
                    student_semester_num = int(''.join(filter(str.isdigit, semester_num)))
                except:
                    student_semester_num = 3
        else:
            student_semester_num = int(student_semester) if student_semester else 3
        
        exam_sessions = list(exam_sessions_collection.find({
            "$or": [
                {"sem": student_semester_text},
                {"sem": student_semester_num}
            ]
        }))
        
        print(f"📊 Found {len(exam_sessions)} exam sessions")
        
        if not exam_sessions:
            raise HTTPException(status_code=404, detail=f"No exam sessions found for semester {student_semester}")
        
        # FIX PHOTO PATH HANDLING
        raw_photo_path = student.get("pic", "")
        print(f"📸 Raw photo path from DB: '{raw_photo_path}'")
        
        # Convert relative path to absolute path
        if raw_photo_path:
            # Handle different path formats
            photo_paths_to_try = [
                raw_photo_path,  # Original path from DB
                f"static/student_images/{raw_photo_path}",  # Add static prefix
                f"pyBackend/static/student_images/{raw_photo_path}",  # Full path
                f"../static/student_images/{raw_photo_path}",  # Relative path
            ]
            
            final_photo_path = ""
            for path in photo_paths_to_try:
                if os.path.exists(path):
                    final_photo_path = path
                    print(f"✅ Found photo at: {path}")
                    break
            
            if not final_photo_path:
                print(f"❌ Photo not found at any path for: {raw_photo_path}")
        else:
            final_photo_path = ""
            print("❌ No photo path in student record")
        
        # Prepare student data with corrected photo path
        student_data = {
            "name": student.get("student_name", ""),
            "roll_number": student.get("reg_no", ""),
            "semester": student.get("sem", ""),
            "branch": student.get("branch", ""),
            "course": student.get("course", ""),
            "year": student.get("year", ""),
            "dob": student.get("dob", ""),
            "contact_no": student.get("contact_no", ""),
            "email_id": student.get("email_id", ""),
            "pic": final_photo_path  # Use the corrected path
        }
        
        # Prepare exam data for ALL sessions
        all_exam_data = []
        for exam_session in exam_sessions:
            subject_code = exam_session.get("subject_code", "")
            subject_name = ""
            
            if subject_code:
                subject_doc = subjects_collection.find_one({"subject_code": subject_code})
                if subject_doc:
                    subject_name = subject_doc.get("subject_name", "")
            
            if not subject_name:
                subject_name = subject_code
            
            exam_data = {
                "subject_code": subject_code,
                "subject_name": subject_name,
                "exam_date": exam_session.get("exam_date", ""),
                "exam_time": exam_session.get("exam_time", "")
            }
            all_exam_data.append(exam_data)
        
        # Generate PDF
        from admit_card_generator import generate_admit_card
        pdf_buffer = generate_admit_card(student_data, all_exam_data)
        
        student_name_clean = student_name.replace(" ", "_")
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=admit_card_{student_name_clean}.pdf"}
        )
        
    except Exception as e:
        print(f"❌ Error generating admit card: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating admit card: {str(e)}")

@app.get("/test-pdf")
async def test_pdf():
    """Test PDF generation without database"""
    try:
        from admit_card_generator import generate_admit_card
        
        test_student = {
            "name": "Test Student",
            "roll_number": "TEST001", 
            "semester": "3rd Semester",
            "course": "B.Tech",
            "branch": "CSE - CS"
        }
        
        test_exam = {
            "subject_code": "21CSC201J",  # ✅ Add subject_code
            "subject_name": "DATA STRUCTURES AND ALGORITHMS",  # ✅ Add subject_name
            "exam_date": "2024-12-15",
            "exam_time": "Morning"
        }
        
        pdf_buffer = generate_admit_card(test_student, test_exam)
        
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=test_admit_card.pdf"}
        )
    except Exception as e:
        print(f"❌ Test PDF Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test PDF failed: {str(e)}")

@app.get("/test-data/")
async def test_data():
    """Test endpoint to check if we can insert and retrieve data"""
    if not MONGO_AVAILABLE:
        return {"error": "MongoDB not available"}
    
    try:
        # Insert test data using "sem" field
        test_subject = {
            "subject_code": "TEST101",
            "subject_name": "Test Subject",
            "sem": 1
        }
        result = subjects_collection.insert_one(test_subject)
        
        # Retrieve it
        subject = subjects_collection.find_one({"_id": result.inserted_id})
        subject = convert_objectid(subject)
        
        return {
            "message": "Data test successful",
            "inserted_id": str(result.inserted_id),
            "retrieved_subject": subject
        }
    except Exception as e:
        return {"error": f"Test failed: {str(e)}"}
    
@app.delete("/exam-sessions/")
async def delete_exam_sessions(sem: int = None):
    """Delete exam sessions, optionally filtered by semester"""
    if not MONGO_AVAILABLE:
        raise HTTPException(status_code=500, detail="MongoDB not available")
    
    try:
        # Handle both text and numeric semester formats
        if sem is not None:
            # Convert numeric semester to text format for querying
            semester_text_map = {
                1: "1st Semester",
                2: "2nd Semester", 
                3: "3rd Semester",
                4: "4th Semester",
                5: "5th Semester",
                6: "6th Semester", 
                7: "7th Semester",
                8: "8th Semester"
            }
            semester_text = semester_text_map.get(sem, f"{sem}th Semester")
            
            # Query for both formats
            query = {
                "$or": [
                    {"sem": sem},
                    {"sem": semester_text}
                ]
            }
        else:
            query = {}
            
        result = exam_sessions_collection.delete_many(query)
        return {"message": f"Deleted {result.deleted_count} exam session(s)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting exam sessions: {str(e)}")

@app.get("/health/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mongo_connected": MONGO_AVAILABLE,
        "service": "Exam Portal API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/debug-students/")
async def debug_students():
    """Debug endpoint to check student data structure"""
    if not MONGO_AVAILABLE:
        return {"error": "MongoDB not available"}
    
    try:
        # Get first few students to see the field names
        students = list(students_collection.find().limit(3))
        students = [convert_objectid(student) for student in students]
        
        return {
            "total_students": students_collection.count_documents({}),
            "sample_students": students,
            "field_names": list(students[0].keys()) if students else []
        }
    except Exception as e:
        return {"error": f"Debug failed: {str(e)}"}
    
@app.get("/debug-exam-sessions/")
async def debug_exam_sessions():
    """Debug endpoint to check all exam sessions"""
    if not MONGO_AVAILABLE:
        return {"error": "MongoDB not available"}
    
    try:
        # Get all exam sessions
        sessions = list(exam_sessions_collection.find())
        sessions = [convert_objectid(session) for session in sessions]
        
        return {
            "total_sessions": len(sessions),
            "sessions": sessions
        }
    except Exception as e:
        return {"error": f"Debug failed: {str(e)}"}