from fastapi import FastAPI, HTTPException
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
async def get_students(semester: int = None):
    """Get students, optionally filtered by semester"""
    if not MONGO_AVAILABLE:
        return {"error": "MongoDB not available", "students": []}
    
    try:
        # Use "sem" field to match your MongoDB data
        query = {"semester": semester} if semester is not None else {}
        students = list(students_collection.find(query))
        students = [convert_objectid(student) for student in students]
        return {"students": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching students: {str(e)}")

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