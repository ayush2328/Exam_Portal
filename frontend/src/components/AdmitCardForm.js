import React, { useState, useEffect } from "react";
import { apiService } from "../services/api";  // Correct path

const AdmitCardForm = ({ setAdmitCardData }) => {
  const [regNo, setRegNo] = useState("");
  const [name, setName] = useState("");
  const [subject, setSubject] = useState("");
  const [examDate, setExamDate] = useState("");
  const [semester, setSemester] = useState("1");
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch subjects from backend when semester changes
  useEffect(() => {
    const fetchSubjects = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await apiService.getSubjects(semester);
        setSubjects(data);
      } catch (error) {
        setError("Failed to load subjects. Please try again.");
        console.error("Error fetching subjects:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSubjects();
  }, [semester]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validate form
    if (!regNo || !subject || !examDate) {
      setError("Please fill in all required fields");
      return;
    }

    // Find the selected subject details
    const selectedSubject = subjects.find(sub => sub.code === subject);
    
    const studentData = {
      name: name || "Ayush Gupta",
      regNo: regNo || "RA241103003034",
      program: "B.Tech - CSE - CS/A",
      examDate: examDate,
      subject: subject,
      subjectName: selectedSubject ? selectedSubject.name : "",
      semester: semester
    };
    
    setAdmitCardData(studentData);
  };

  return (
    <form onSubmit={handleSubmit} className="admit-card-form">
      <h3>Generate Admit Card</h3>
      
      {error && <div className="error-message">{error}</div>}

      {/* Semester Selection */}
      <div className="form-group">
        <label>Select Semester:</label>
        <select 
          value={semester} 
          onChange={(e) => setSemester(e.target.value)}
          required
        >
          <option value="1">Semester 1</option>
          <option value="2">Semester 2</option>
          <option value="3">Semester 3</option>
        </select>
      </div>

      {/* Registration Number */}
      <div className="form-group">
        <input
          type="text"
          placeholder="Registration Number *"
          value={regNo}
          onChange={(e) => setRegNo(e.target.value)}
          required
        />
      </div>

      {/* Student Name */}
      <div className="form-group">
        <input
          type="text"
          placeholder="Student Name *"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>

      {/* Subject Selection */}
      <div className="form-group">
        <label>Select Subject *:</label>
        {loading ? (
          <p>Loading subjects...</p>
        ) : (
          <select
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            required
          >
            <option value="">Select a subject</option>
            {subjects.map((sub) => (
              <option key={sub.code} value={sub.code}>
                {sub.code} - {sub.name}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* Exam Date */}
      <div className="form-group">
        <label>Exam Date *:</label>
        <input
          type="date"
          value={examDate}
          onChange={(e) => setExamDate(e.target.value)}
          required
        />
      </div>

      <button type="submit" disabled={loading}>
        {loading ? "Loading..." : "Preview Admit Card"}
      </button>

      {/* Display available subjects count */}
      {!loading && subjects.length > 0 && (
        <p className="subject-count">
          {subjects.length} subjects available for Semester {semester}
        </p>
      )}
    </form>
  );
};

export default AdmitCardForm;