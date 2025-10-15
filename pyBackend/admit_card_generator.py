from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import io
import os
from datetime import datetime

def generate_admit_card(student_data, exam_data_list):
    """
    Generates an SRM-style admit card PDF with static logos and dynamic student photo.
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- Paths for static logos ---
    SRM_LOGO_PATH = "static/srm_logo.png"
    IEC_LOGO_PATH = "static/iec_stamp.png"

    # --- Header Section ---
    try:
        if os.path.exists(SRM_LOGO_PATH):
            # Calculate scaled dimensions to fit nicely in top right corner
            # Original size: 386x131, scaling to appropriate size for A4
            logo_width = 120  # Scaled width
            logo_height = 46  # Scaled height (maintaining aspect ratio: 100 * 131/386 ≈ 34)
            
            # Position at top right corner with some margin
            pdf.drawImage(SRM_LOGO_PATH, width - logo_width - 10, height - logo_height - 10, 
                        width=logo_width, height=logo_height, mask='auto')
        else:
            pdf.setFont("Helvetica-Bold", 12)
            # Position text placeholder at top right
            pdf.drawString(width - 140, height - 60, "SRM LOGO")
    except Exception as e:
        print(f"⚠️ Could not load SRM logo: {e}")

    # pdf.setFont("Helvetica-Bold", 16)
    # pdf.drawCentredString(width / 2, height - 140, "SRM INSTITUTE OF SCIENCE AND TECHNOLOGY")
    # pdf.setFont("Helvetica", 12)
    # pdf.drawCentredString(width / 2, height - 160, "DELHI-NCR CAMPUS, GHAZIABAD (U.P)")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(width / 2, height - 120, "Internal Examinations - I, September 2025")
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(width / 2, height - 140, "HALL TICKET")

    # Serial Number
    pdf.setFont("Helvetica-Bold", 10)
    serial_no = f"Serial No.: 25/{student_data.get('roll_number', '').replace('RA', '')}"
    pdf.drawString(50, height - 180, serial_no)

   # --- Student Details Section with Box ---
    y = height - 200

    # Draw the box around student details
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    pdf.rect(40, y - 90, width - 80, 100)  # Box around all student details

    # Student details with bullet points inside the box
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(60, y, "EXAMINATION CENTRE")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(250, y, "SRMIST, Delhi-NCR Campus")

    y -= 25
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(60, y, "NAME OF THE CANDIDATE")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(250, y, student_data.get('name', '').upper())

    y -= 25
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(60, y, "REGISTRATION NUMBER")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(250, y, student_data.get('roll_number', ''))

    y -= 25
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(60, y, "PROGRAM/SECTION")
    pdf.setFont("Helvetica", 10)
    program = f"{student_data.get('course', 'B.Tech')} - {student_data.get('branch', 'CSE - CS')}/A"
    pdf.drawString(250, y, program.upper())

    # Draw bullet points (•)
    bullet_x = 45
    pdf.setFont("Helvetica", 14)
    pdf.drawString(bullet_x, y + 75,"")  # For EXAMINATION CENTRE
    pdf.drawString(bullet_x, y + 50,"")  # For NAME
    pdf.drawString(bullet_x, y + 25,"")  # For REGISTRATION NUMBER
         # For PROGRAM/SECTION

    # --- Student Photo with Box ---
    photo_drawn = False
    photo_paths = [
        student_data.get('photo', ''),
        student_data.get('pic', ''),
        f"pyBackend/static/student_images/{student_data.get('roll_number', '')}.jpg",
        f"static/student_images/{student_data.get('roll_number', '')}.jpg",
    ]

    for p in photo_paths:
        if p and os.path.exists(p):
            try:
                # Draw the photo box
                pdf.setStrokeColor(colors.black)
                # pdf.setLineWidth(1)
                # pdf.rect(width - 116, height - 300, 75, 100)
                # Draw the photo inside the box
                pdf.drawImage(ImageReader(p), width - 116, height - 280, width=75, height=100, preserveAspectRatio=True, mask='auto')
                photo_drawn = True
                break
            except Exception as e:
                print(f"⚠️ Could not load student photo: {e}")

    if not photo_drawn:
        # Draw empty photo box
        pdf.setStrokeColor(colors.black)
        # pdf.setLineWidth(1)
        pdf.rect(width - 130, height - 230, 80, 90)
        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(width - 80, height - 280, "PHOTO")

    # --- Table Header ---
    y -= 60
    pdf.setLineWidth(1)
    pdf.line(40, y, width - 40, y)

    y -= 20
    pdf.setFont("Helvetica-Bold", 10)
    headers = ["SEMESTER", "SUB. CODE", "SUBJECT", "DATE OF EXAM", "SESSION"]
    col_x = [50, 120, 180, 420, 510]
    for i, h in enumerate(headers):
        pdf.drawString(col_x[i], y, h)

    pdf.line(40, y - 5, width - 40, y - 5)

    # --- Table Rows ---
    pdf.setFont("Helvetica", 9)
    y -= 20
    semester = student_data.get('', 'III').replace('3rd', ' III').upper()

    for exam in exam_data_list:
        if y < 100:
            pdf.showPage()
            y = height - 100

        sub_code = exam.get('subject_code', '')
        sub_name = exam.get('subject_name', '')
        date = exam.get('exam_date', '')
        session = "FN" if exam.get('exam_time', '').lower() == "morning" else "AN"

        pdf.drawString(col_x[0], y, semester)
        pdf.drawString(col_x[1], y, sub_code)
        pdf.drawString(col_x[2], y, sub_name[:30])  # truncate long names
        pdf.drawString(col_x[3], y, date)
        pdf.drawString(col_x[4], y, session)
        y -= 20

    pdf.line(40, y + 10, width - 40, y + 10)

    # --- Footer Section ---
    y -= 20
    pdf.setFont("Helvetica-Bold", 10)
    pdf.setFillColor(colors.red)
    pdf.drawCentredString(width / 2, y, "**** End of Statement ****")

    # --- Signatures ---
    y -= 40
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(60, y, "SIGNATURE OF THE CANDIDATE")
    pdf.drawString(width - 180, y, "HEAD - IEC")

    y -= 20
    pdf.line(60, y, 220, y)
    pdf.line(width - 180, y, width - 60, y)
    pdf.line(width - 180, y, width - 60, y)   
    y -= 200
    pdf.setLineWidth(1)
    pdf.line(40, y, width - 40, y)
    # IEC Stamp
    try:
        if os.path.exists(IEC_LOGO_PATH):
            pdf.drawImage(IEC_LOGO_PATH, 20, height - 80, width=80, height=75, mask='auto')
        else:
            pdf.setFont("Helvetica-Bold", 12)
        # pdf.drawString(40, height - 80, "IEC LOGO")
    except Exception as e:
        print(f"⚠️ Could not load IEC logo: {e}")

    # Footer date
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.setFillColor(colors.grey)
    pdf.drawCentredString(width / 2, 40, "Generated on: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    pdf.save()
    buffer.seek(0)
    return buffer
   
    pdf.line(width - 180, y, width - 60, y)

if __name__ == "__main__":
    student = {
        "name": "Ayush Gupta",
        "roll_number": "RA241103003034",
        "course": "B.Tech",
        "branch": "CSE - CS",
        "semester": "3rd Semester"
    }

    exams = [
        {"subject_code": "21MAB206T", "subject_name": "NUMERICAL METHODS AND ANALYSIS", "exam_date": "01.09.2025", "exam_time": "Morning"},
        {"subject_code": "21CSC203P", "subject_name": "ADVANCED PROGRAMMING PRACTICE", "exam_date": "02.09.2025", "exam_time": "Morning"},
        {"subject_code": "21CSC201T", "subject_name": "COMPUTER ORGANIZATION AND ARCHITECTURE", "exam_date": "03.09.2025", "exam_time": "Morning"},
        {"subject_code": "21CSC201J", "subject_name": "DATA STRUCTURES AND ALGORITHMS", "exam_date": "04.09.2025", "exam_time": "Morning"},
        {"subject_code": "21CSC202J", "subject_name": "OPERATING SYSTEMS", "exam_date": "08.09.2025", "exam_time": "Morning"},
    ]

    pdf_buffer = generate_admit_card(student, exams)
    with open("Ayush_Gupta_HallTicket.pdf", "wb") as f:
        f.write(pdf_buffer.getvalue())
    print("✅ Admit card generated: Ayush_Gupta_HallTicket.pdf")
