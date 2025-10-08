from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
from datetime import datetime

def generate_admit_card(student_data, exam_data_list):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Set up colors
    primary_color = (0.2, 0.4, 0.6)  # Dark blue
    secondary_color = (0.8, 0.9, 1.0)  # Light blue
    accent_color = (0.9, 0.1, 0.1)  # Red for important info
    
    # Header Section with background
    pdf.setFillColorRGB(*primary_color)
    pdf.rect(0, height-60, width, 60, fill=1, stroke=0)
    
    # SRM Logo - Hardcoded (you can replace this with actual SRM logo image)
    try:
        # Draw SRM logo placeholder (you can replace this with actual logo file)
        pdf.setFillColorRGB(1, 1, 1)  # White background for logo
        pdf.rect(50, height-50, 40, 40, fill=1, stroke=1)
        pdf.setFillColorRGB(*primary_color)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(55, height-35, "SRM")
        pdf.drawString(55, height-45, "LOGO")
    except Exception as e:
        print(f"Warning: Could not draw SRM logo: {e}")
    
    # Header text
    pdf.setFillColorRGB(1, 1, 1)  # White text
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, height-30, "Internal Examinations - I, September 2025")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(width/2, height-65, "HALL TICKET")
    
    # Serial Number
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 10)
    serial_no = f"Serial No.: 25/{student_data.get('roll_number', '').replace('RA', '')}"
    pdf.drawString(width-180, height-30, serial_no)
    
    # Line separator after header
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setLineWidth(1)
    pdf.line(40, height-80, width-40, height-80)
    
    # Student Information Section
    y_position = height - 110
    
    # Left column - Examination Centre
    pdf.setFillColorRGB(*primary_color)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y_position, "EXAMINATION CENTRE")
    
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y_position - 20, "SRMIST, Delhi-NCR Campus")
    
    # Registration Number
    pdf.setFillColorRGB(*primary_color)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y_position - 45, "REGISTRATION NUMBER")
    
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y_position - 60, student_data.get('roll_number', ''))
    
    # Right column - Name and Program
    pdf.setFillColorRGB(*primary_color)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(width/2, y_position, "NAME OF THE CANDIDATE")
    
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica-Bold", 10)
    student_name = student_data.get('name', '').upper()
    pdf.drawString(width/2, y_position - 20, student_name)
    
    # Program/Section
    pdf.setFillColorRGB(*primary_color)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(width/2, y_position - 45, "PROGRAM/SECTION")
    
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 10)
    program_section = f"{student_data.get('course', 'BTECH')} - {student_data.get('branch', 'CSE - CS')}/A"
    pdf.drawString(width/2, y_position - 60, program_section.upper())
    
    # Student Photo Section (Dynamic for each student)
    photo_drawn = False
    
    # Try to load student photo from multiple possible locations
    photo_paths_to_try = [
        student_data.get('pic', ''),
        student_data.get('photo', ''),
        student_data.get('image', ''),
        f"photos/{student_data.get('roll_number', '')}.jpg",
        f"images/{student_data.get('roll_number', '')}.jpg",
        f"student_photos/{student_data.get('roll_number', '')}.jpg"
    ]
    
    for photo_path in photo_paths_to_try:
        if photo_path and os.path.exists(photo_path):
            try:
                # Draw student photo
                img = ImageReader(photo_path)
                pdf.drawImage(img, width-100, y_position-80, width=80, height=80, preserveAspectRatio=True, mask='auto')
                photo_drawn = True
                print(f"✅ Student photo loaded: {photo_path}")
                break
            except Exception as e:
                print(f"⚠️ Could not load student photo from {photo_path}: {e}")
                continue
    
    # If no student photo found, draw default photo placeholder
    if not photo_drawn:
        try:
            # Try to load a default photo if exists
            default_photos = [
                "default_student_photo.jpg",
                "images/default_photo.jpg", 
                "photos/default.jpg",
                "default_photo.png"
            ]
            
            default_loaded = False
            for default_photo in default_photos:
                if os.path.exists(default_photo):
                    img = ImageReader(default_photo)
                    pdf.drawImage(img, width-100, y_position-80, width=80, height=80, preserveAspectRatio=True, mask='auto')
                    default_loaded = True
                    print(f"✅ Default photo loaded: {default_photo}")
                    break
            
            if not default_loaded:
                # Draw photo placeholder with student initial
                pdf.setFillColorRGB(0.8, 0.9, 1.0)  # Light blue background
                pdf.rect(width-100, y_position-80, 80, 80, fill=1, stroke=1)
                pdf.setFillColorRGB(*primary_color)
                pdf.setFont("Helvetica-Bold", 16)
                
                # Get student initial for placeholder
                student_name = student_data.get('name', 'S')
                initial = student_name[0].upper() if student_name else 'S'
                pdf.drawCentredString(width-60, y_position-40, initial)
                
                pdf.setFillColorRGB(0.5, 0.5, 0.5)
                pdf.setFont("Helvetica", 6)
                pdf.drawCentredString(width-60, y_position-55, "PHOTO")
                print("✅ Default photo placeholder drawn with initial")
                
        except Exception as e:
            print(f"❌ Error creating default photo: {e}")
            # Final fallback - simple rectangle
            pdf.setFillColorRGB(0.9, 0.9, 0.9)
            pdf.rect(width-100, y_position-80, 80, 80, fill=1, stroke=1)
            pdf.setFillColorRGB(0.5, 0.5, 0.5)
            pdf.setFont("Helvetica", 8)
            pdf.drawCentredString(width-60, y_position-40, "PHOTO")
    
    # Line separator before table
    y_position -= 100
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.line(40, y_position, width-40, y_position)
    
    # Exam Schedule Table
    y_position -= 30
    
    # Table Header
    pdf.setFillColorRGB(*primary_color)
    pdf.setFont("Helvetica-Bold", 10)
    
    # Define column positions and widths
    col_positions = [50, 130, 280, 430, 500]  # x positions for columns
    col_widths = [60, 120, 120, 50, 40]  # widths for text wrapping
    
    headers = ["SEMESTER", "SUBJECT CODE", "SUBJECT NAME", "DATE", "SESSION"]
    
    for i, header in enumerate(headers):
        if i == 2:  # Subject Name column
            pdf.drawString(col_positions[i], y_position, "SUBJECT")
        else:
            pdf.drawString(col_positions[i], y_position, header)
    
    # Line under header
    y_position -= 5
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setLineWidth(0.5)
    pdf.line(40, y_position, width-40, y_position)
    
    # Table rows - USE ALL EXAM DATA
    y_position -= 15
    
    # Convert semester number to roman numeral
    semester_num = student_data.get('semester', '3')
    if isinstance(semester_num, str) and 'Semester' in semester_num:
        semester_roman = semester_num.replace('Semester', '').strip()
        if semester_roman == '3rd':
            semester_roman = 'III'
        elif semester_roman == '2nd':
            semester_roman = 'II'
        elif semester_roman == '1st':
            semester_roman = 'I'
        else:
            semester_roman = semester_roman.upper()
    else:
        semester_map = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII'}
        semester_roman = semester_map.get(int(semester_num), str(semester_num))
    
    # Create exam schedule with ALL submitted exams
    exam_schedule = []
    
    # Handle both single exam (old format) and multiple exams (new format)
    if isinstance(exam_data_list, dict):
        # Single exam (backward compatibility)
        exam_data_list = [exam_data_list]
    
    for exam_data in exam_data_list:
        # Format date from "2024-12-15" to "15.12.2024"
        exam_date = exam_data.get('exam_date', '')
        if exam_date and '-' in exam_date:
            try:
                date_parts = exam_date.split('-')
                if len(date_parts) == 3:
                    formatted_date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"
                else:
                    formatted_date = exam_date
            except:
                formatted_date = exam_date
        else:
            formatted_date = exam_date
        
        # Format session (FN for Morning, AN for Afternoon)
        exam_time = exam_data.get('exam_time', '')
        session_code = "FN" if exam_time.lower() == "morning" else "AN"
        
        exam_schedule.append({
            "sem": semester_roman, 
            "code": exam_data.get('subject_code', exam_data.get('subject_name', '')), 
            "subject": exam_data.get('subject_name', ''), 
            "date": formatted_date, 
            "session": session_code
        })
    
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica", 8)
    
    for exam in exam_schedule:
        # Check if we need a new page
        if y_position < 100:
            pdf.showPage()
            
            # Redraw header with SRM logo on new page
            pdf.setFillColorRGB(*primary_color)
            pdf.rect(0, height-60, width, 60, fill=1, stroke=0)
            
            # SRM Logo on new page
            try:
                pdf.setFillColorRGB(1, 1, 1)
                pdf.rect(50, height-50, 40, 40, fill=1, stroke=1)
                pdf.setFillColorRGB(*primary_color)
                pdf.setFont("Helvetica-Bold", 10)
                pdf.drawString(55, height-35, "SRM")
                pdf.drawString(55, height-45, "LOGO")
            except:
                pass
            
            pdf.setFillColorRGB(1, 1, 1)
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(100, height-30, "Internal Examinations - I, September 2025 - Contd.")
            
            # Redraw table header on new page
            y_position = height - 80
            pdf.setFillColorRGB(*primary_color)
            pdf.setFont("Helvetica-Bold", 10)
            for i, header in enumerate(headers):
                if i == 2:
                    pdf.drawString(col_positions[i], y_position, "SUBJECT")
                else:
                    pdf.drawString(col_positions[i], y_position, header)
            y_position -= 5
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.setLineWidth(0.5)
            pdf.line(40, y_position, width-40, y_position)
            y_position -= 15
        
        # Semester
        pdf.drawString(col_positions[0], y_position, exam["sem"])
        
        # Subject Code
        pdf.drawString(col_positions[1], y_position, exam["code"])
        
        # Subject Name (with word wrapping)
        subject_name = exam["subject"]
        # Split long subject names
        if len(subject_name) > 25:
            words = subject_name.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + " " + word) <= 25:
                    current_line += " " + word if current_line else word
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            
            # Draw multiple lines for long subject names
            line_height = y_position
            for i, line in enumerate(lines):
                pdf.drawString(col_positions[2], line_height - (i * 10), line)
            
            # Adjust y_position based on number of lines
            y_position_adjustment = max(len(lines) - 1, 0) * 10
            y_position -= (25 + y_position_adjustment)
        else:
            pdf.drawString(col_positions[2], y_position, subject_name)
            y_position -= 25
        
        # Date
        pdf.drawString(col_positions[3], y_position + 25, exam["date"])
        
        # Session
        pdf.drawString(col_positions[4], y_position + 25, exam["session"])
    
    # End of statement
    y_position -= 30
    pdf.setFillColorRGB(*accent_color)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(width/2, y_position, "*** End of Statement ***")
    
    # Line separator
    y_position -= 15
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.line(40, y_position, width-40, y_position)
    
    # Signatures section
    y_position -= 40
    
    # Candidate signature
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y_position, "SIGNATURE OF THE CANDIDATE")
    
    # Head - IEC
    pdf.drawString(width-150, y_position, "HEAD - IEC")
    
    # Signature lines
    y_position -= 20
    pdf.setStrokeColorRGB(0, 0, 0)
    pdf.setLineWidth(0.5)
    pdf.line(50, y_position, 200, y_position)  # Candidate line
    pdf.line(width-150, y_position, width-50, y_position)  # IEC line
    
    # Footer note
    y_position -= 30
    pdf.setFillColorRGB(0.5, 0.5, 0.5)
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawCentredString(width/2, y_position, "Generated on: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    pdf.save()
    buffer.seek(0)
    return buffer

# Create a default student photo (you can replace this with actual default image)
def create_default_photo_if_not_exists():
    """Create a simple default photo if it doesn't exist"""
    default_photo_path = "default_student_photo.jpg"
    if not os.path.exists(default_photo_path):
        try:
            # Create a simple default photo using reportlab
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.colors import lightblue, darkblue
            
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=(200, 200))
            c.setFillColor(lightblue)
            c.rect(0, 0, 200, 200, fill=1, stroke=0)
            c.setFillColor(darkblue)
            c.setFont("Helvetica-Bold", 40)
            c.drawCentredString(100, 90, "SRM")
            c.setFont("Helvetica", 15)
            c.drawCentredString(100, 50, "Student")
            c.save()
            
            # Convert to image (this is a simplified approach)
            # In production, you should use an actual default image file
            print("ℹ️  Please add a proper default_student_photo.jpg file")
            
        except Exception as e:
            print(f"Note: Could not create default photo: {e}")

# Test function for multiple subjects
def test_multiple_subjects():
    """Test function for multiple exam sessions"""
    # Test data for multiple subjects with different photo scenarios
    test_students = [
        {
            "name": "Keshav Chauhan",
            "roll_number": "RA2411030030001",
            "course": "B.Tech",
            "branch": "CSE - CS",
            "semester": "3rd Semester",
            "pic": "pic_01.png"  # Existing photo
        },
        {
            "name": "Raj Aryan", 
            "roll_number": "RA2411030030002",
            "course": "B.Tech",
            "branch": "CSE - CS",
            "semester": "3rd Semester",
            "pic": ""  # No photo - should use default
        },
        {
            "name": "Sushant Bhardwaj",
            "roll_number": "RA2411030030003", 
            "course": "B.Tech",
            "branch": "CSE - CS",
            "semester": "3rd Semester"
            # No pic field at all - should use default
        }
    ]
    
    # Multiple exam sessions
    test_exams = [
        {
            "subject_code": "21CSC201J",
            "subject_name": "DATA STRUCTURES AND ALGORITHMS",
            "exam_date": "2024-12-15",
            "exam_time": "Morning"
        },
        {
            "subject_code": "21CSC202J", 
            "subject_name": "OPERATING SYSTEMS",
            "exam_date": "2024-12-16",
            "exam_time": "Afternoon"
        }
    ]
    
    # Generate admit cards for all test students
    for i, student in enumerate(test_students):
        pdf_buffer = generate_admit_card(student, test_exams)
        
        # Save test PDF
        filename = f"test_admit_card_{i+1}_{student['name'].replace(' ', '_')}.pdf"
        with open(filename, "wb") as f:
            f.write(pdf_buffer.getvalue())
        
        print(f"✅ Admit card generated: {filename}")

# Test function for single subject
def test_single_subject():
    """Test function for single exam session"""
    test_student = {
        "name": "Test Student",
        "roll_number": "RA2411030030001",
        "course": "B.Tech",
        "branch": "CSE - CS",
        "semester": "3rd Semester",
        "pic": "non_existent_photo.jpg"  # Non-existent photo
    }
    
    test_exam = {
        "subject_code": "21CSC201J",
        "subject_name": "DATA STRUCTURES AND ALGORITHMS", 
        "exam_date": "2024-12-15",
        "exam_time": "Morning"
    }
    
    pdf_buffer = generate_admit_card(test_student, test_exam)
    
    with open("single_subject_admit_card.pdf", "wb") as f:
        f.write(pdf_buffer.getvalue())
    
    print("✅ Single subject admit card generated: single_subject_admit_card.pdf")

if __name__ == "__main__":
    # Create default photo if needed
    create_default_photo_if_not_exists()
    
    # Run tests
    test_single_subject()
    test_multiple_subjects()
    print("🎫 All test admit cards generated successfully!")
    print("\n📝 Note: To use actual SRM logo, replace the logo placeholder with:")
    print("   - Add 'srm_logo.png' file in the same directory")
    print("   - Update the code to use: ImageReader('srm_logo.png')")