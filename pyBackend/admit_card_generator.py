from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_admit_card(student_data, exam_data):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    
    # Add content to PDF
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 800, "EXAM ADMIT CARD")
    
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 750, f"Student Name: {student_data.get('name', '')}")
    pdf.drawString(100, 730, f"Roll Number: {student_data.get('roll_number', '')}")
    pdf.drawString(100, 710, f"Semester: {student_data.get('semester', '')}")
    
    pdf.drawString(100, 670, f"Subject: {exam_data.get('subject_name', '')}")
    pdf.drawString(100, 650, f"Date: {exam_data.get('exam_date', '')}")
    pdf.drawString(100, 630, f"Time: {exam_data.get('exam_time', '')}")
    
    pdf.save()
    buffer.seek(0)
    return buffer