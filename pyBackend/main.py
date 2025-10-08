from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
import os
import json

app = FastAPI(title="Exam Portal API", version="1.0.0")

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
        # Convert numeric semester to text format if provided
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
        students = [convert_objectid(student) for student in students]
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
        
        # Get student data using _id (MongoDB ObjectId)
        student = students_collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            print("❌ Student not found in database")
            raise HTTPException(status_code=404, detail="Student not found")
        
        print(f"✅ Found student: {student.get('student_name', 'Unknown')}")
        
        # Get exam data for the student's semester
        student_semester = student.get("sem", "")
        print(f"🔍 Looking for ALL exam sessions for semester: {student_semester}")
        
        # Get ALL exam sessions for this semester, not just one
        exam_sessions = list(exam_sessions_collection.find({
            "sem": student_semester
        }))
        
        print(f"📊 Found {len(exam_sessions)} exam sessions for semester {student_semester}")
        
        if not exam_sessions:
            print("❌ No exam sessions found for student's semester")
            print("🔄 Creating default exam session...")
            # Create a default exam session
            default_exam = {
                "subject_code": "21CSC201J",
                "exam_date": "2024-12-15", 
                "exam_time": "Morning",
                "sem": student_semester
            }
            exam_sessions_collection.insert_one(default_exam)
            exam_sessions = [default_exam]
            print("✅ Created default exam session")
        
        # Prepare student data
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
            "pic": student.get("pic", "")  # Add photo path if available
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
            
            # If subject name not found, use a default based on code
            if not subject_name:
                # Map common subject codes to names
                subject_name_map = {
                    "21CSC201J": "DATA STRUCTURES AND ALGORITHMS",
                    "21CSC202J": "OPERATING SYSTEMS", 
                    "21CSC203P": "ADVANCED PROGRAMMING PRACTICE",
                    "21CSS201T": "COMPUTER ORGANIZATION AND ARCHITECTURE",
                    "21MAB206T": "NUMERICAL METHODS AND ANALYSIS"
                }
                subject_name = subject_name_map.get(subject_code, f"Subject {subject_code}")
                print(f"⚠️  Subject name not found for code {subject_code}, using mapped name")
            
            exam_data = {
                "subject_code": subject_code,
                "subject_name": subject_name,
                "exam_date": exam_session.get("exam_date", ""),
                "exam_time": exam_session.get("exam_time", "")
            }
            all_exam_data.append(exam_data)
            print(f"📅 Added exam session: {exam_data}")
        
        print(f"📄 Student data for PDF: {student_data}")
        print(f"📅 All exam data for PDF: {all_exam_data}")
        
        # Generate PDF with ALL exam sessions
        print("🔄 Importing PDF generator...")
        from admit_card_generator import generate_admit_card
        print("✅ PDF generator imported")
        
        print("🔄 Generating PDF with multiple sessions...")
        pdf_buffer = generate_admit_card(student_data, all_exam_data)
        print("✅ PDF generated successfully")
        
        student_name = student.get("student_name", "student").replace(" ", "_")
        print(f"📤 Returning PDF response for: {student_name}")
        
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=admit_card_{student_name}.pdf"}
        )
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR in admit card generation:")
        print(f"❌ Error type: {type(e).__name__}")
        print(f"❌ Error message: {str(e)}")
        import traceback
        print(f"❌ Full traceback:")
        traceback.print_exc()
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