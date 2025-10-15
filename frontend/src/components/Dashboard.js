import React, { useState, useEffect } from "react";
import { apiService } from "../services/api";
import "./Dashboard.css";

function Dashboard() {
  const [semester, setSemester] = useState("");
  const [branch, setBranch] = useState("Cyber Security");
  const [internalExam, setInternalExam] = useState("");
  const [year, setYear] = useState(new Date().getFullYear());
  const [month, setMonth] = useState("");
  const [availableSubjects, setAvailableSubjects] = useState([]);
  const [selectedSubjects, setSelectedSubjects] = useState([]);
  const [subjectSessions, setSubjectSessions] = useState({});
  const [availableDates, setAvailableDates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // New states for admit card generation
  const [recentExamSession, setRecentExamSession] = useState(null);
  const [studentsForRecentExam, setStudentsForRecentExam] = useState([]);
  const [admitCardLoading, setAdmitCardLoading] = useState(false);
  const [showAdmitCardSection, setShowAdmitCardSection] = useState(false);

  // Generate years (current year and next 2 years)
  const years = Array.from({ length: 3 }, (_, i) => new Date().getFullYear() + i);

  // Months list
  const months = [
    { value: "01", name: "January" }, { value: "02", name: "February" },
    { value: "03", name: "March" }, { value: "04", name: "April" },
    { value: "05", name: "May" }, { value: "06", name: "June" },
    { value: "07", name: "July" }, { value: "08", name: "August" },
    { value: "09", name: "September" }, { value: "10", name: "October" },
    { value: "11", name: "November" }, { value: "12", name: "December" }
  ];

  // Generate available dates when month and year are selected
  useEffect(() => {
    if (month && year) {
      const daysInMonth = new Date(year, month, 0).getDate();
      const dates = Array.from({ length: daysInMonth }, (_, i) => i + 1);
      setAvailableDates(dates);
    } else {
      setAvailableDates([]);
    }
  }, [month, year]);

  // Fetch subjects from backend when semester changes
  useEffect(() => {
    if (semester) {
      setLoading(true);
      setError("");
      apiService.getSubjects(semester)
        .then(data => {
          setAvailableSubjects(data);
          setSelectedSubjects([]);
          setSubjectSessions({});
          setLoading(false);
        })
        .catch(err => {
          console.error('Error fetching subjects:', err);
          setError('Failed to load subjects. Please try again.');
          setLoading(false);
          setAvailableSubjects([]);
        });
    } else {
      setAvailableSubjects([]);
      setSelectedSubjects([]);
      setSubjectSessions({});
    }
  }, [semester]);

  const handleSubjectSelection = (subjectCode, isSelected) => {
    if (isSelected) {
      const subjectToAdd = availableSubjects.find(sub => sub.code === subjectCode);
      if (subjectToAdd) {
        setSelectedSubjects(prev => [...prev, subjectToAdd]);
        setSubjectSessions(prev => ({
          ...prev,
          [subjectCode]: { date: "", session: "" }
        }));
      }
    } else {
      setSelectedSubjects(prev => prev.filter(sub => sub.code !== subjectCode));
      setSubjectSessions(prev => {
        const newSessions = { ...prev };
        delete newSessions[subjectCode];
        return newSessions;
      });
    }
  };

  const handleSessionChange = (subjectCode, field, value) => {
    setSubjectSessions(prev => ({
      ...prev,
      [subjectCode]: {
        ...prev[subjectCode],
        [field]: value
      }
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (selectedSubjects.length === 0) {
      alert("Please select at least one subject!");
      return;
    }

    const incompleteSubjects = selectedSubjects.filter(subject =>
      !subjectSessions[subject.code]?.date || !subjectSessions[subject.code]?.session
    );

    if (incompleteSubjects.length > 0) {
      alert("Please select date and session for all subjects!");
      return;
    }

    try {
      setLoading(true);

      const submissionPromises = selectedSubjects.map(async (subject) => {
        const examData = {
          subjectCode: subject.code,
          examDate: `${year}-${month}-${subjectSessions[subject.code].date.toString().padStart(2, '0')}`,
          examTime: subjectSessions[subject.code].session,
          semester: parseInt(semester)
        };
        return await apiService.addExamSession(examData);
      });

      const results = await Promise.all(submissionPromises);
      console.log("All exam sessions submitted successfully:", results);

      // FIX: Store ALL exam session IDs, not just the first one
      const examSessionIds = results.map(result => result.id).filter(id => id);
      console.log("🎯 All exam session IDs:", examSessionIds);

      if (examSessionIds.length > 0) {
        // FIX: Load students using the semester (which finds all sessions)
        await loadStudentsForExamSession(examSessionIds[0]); // Still use first ID for API call

        // Show admit card section
        setShowAdmitCardSection(true);
      }

      alert(`Successfully submitted ${selectedSubjects.length} exam session(s)! Admit card generation is now available below.`);

      // Reset form but keep semester
      setInternalExam("");
      setYear(new Date().getFullYear());
      setMonth("");
      setSelectedSubjects([]);
      setSubjectSessions({});

    } catch (error) {
      console.error('Error submitting exam session:', error);
      alert("Error submitting exam session. Please check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const loadStudentsForExamSession = async (examSessionId) => {
    try {
      setAdmitCardLoading(true);
      // FIX: Get students by semester instead of exam session ID
      const data = await apiService.getStudentsBySemester(semester);
      setStudentsForRecentExam(data.students || []);
      console.log('Loaded students for semester:', data.students);
    } catch (error) {
      console.error('Error loading students:', error);
      alert('Error loading students for admit card generation');
    } finally {
      setAdmitCardLoading(false);
    }
  };

  const clearPreviousSessions = async () => {
    try {
      await apiService.clearExamSessions(semester);
      alert("Previous exam sessions cleared!");
    } catch (error) {
      console.error('Error clearing sessions:', error);
    }
  };




  const handleGenerateAdmitCard = async (studentId, studentName) => {
    try {
      setAdmitCardLoading(true);
      await apiService.generateAdmitCard(studentId);
      alert(`Admit card for ${studentName} downloaded successfully! Check your downloads folder.`);
    } catch (error) {
      alert('Error generating admit card: ' + error.message);
    } finally {
      setAdmitCardLoading(false);
    }
  };

  const handleGenerateAllAdmitCards = async () => {
    if (studentsForRecentExam.length === 0) {
      alert("No students available for admit card generation!");
      return;
    }

    try {
      setAdmitCardLoading(true);
      const studentIds = studentsForRecentExam.map(student => student._id);
      await apiService.generateBulkAdmitCards(studentIds);
      alert(`Generated admit cards for all ${studentsForRecentExam.length} students! Check your downloads folder.`);
    } catch (error) {
      alert('Error generating bulk admit cards: ' + error.message);
    } finally {
      setAdmitCardLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Welcome Admin</h2>
      </div>

      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit} className="dashboard-form">
        <div className="form-controls">
          <div className="control-group">
            <label>Semester:</label>
            <select value={semester} onChange={e => setSemester(e.target.value)} required>
              <option value="">Select Semester</option>
              <option value="1">1st</option>
              <option value="2">2nd</option>
              <option value="3">3rd</option>
              <option value="4">4th</option>
              <option value="5">5th</option>
              <option value="6">6th</option>
              <option value="7">7th</option>
              <option value="8">8th</option>
            </select>
          </div>

          <div className="control-group">
            <label>Branch:</label>
            <select value={branch} onChange={e => setBranch(e.target.value)} required>
              <option value="Cyber Security">Cyber Security</option>
              <option value="Cyber Security">Cloud Computing</option>
              <option value="Cyber Security">Data Science</option>
              <option value="Cyber Security">AI/ML</option>
              <option value="Cyber Security">CORE</option>
              <option value="Cyber Security">Bussiness Analytic</option>
              <option value="Cyber Security">Bussiness Studies</option>
              <option value="CSE">CSE</option>
              <option value="ECE">ECE</option>
            </select>
          </div>

          <div className="control-group">
            <label>Internal Exam:</label>
            <select value={internalExam} onChange={e => setInternalExam(e.target.value)} required>
              <option value="">Select Internal Exam</option>
              <option value="1st Internal">1st Internal</option>
              <option value="2nd Internal">2nd Internal</option>
            </select>
          </div>

          <div className="control-group">
            <label>Year:</label>
            <select value={year} onChange={e => setYear(e.target.value)} required>
              {years.map(y => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          </div>

          <div className="control-group">
            <label>Month:</label>
            <select value={month} onChange={e => setMonth(e.target.value)} required>
              <option value="">Select Month</option>
              {months.map(m => (
                <option key={m.value} value={m.value}>{m.name}</option>
              ))}
            </select>
          </div>
        </div>

        {loading ? (
          <p className="loading-text">Loading subjects...</p>
        ) : availableSubjects.length > 0 ? (
          <div className="subjects-section">
            <div className="heading_SubjectSection">
              <h3 className="section-title">
                Select Subjects for Exam 
                <span className="selection-count">{" "+availableSubjects.length} subjects</span>
              </h3>
            </div>
            <div className="subjects-list">
              {availableSubjects.map((subject) => (
                <div key={subject.code} className="subject-item">
                  <label>
                    <input
                      type="checkbox"
                      className="subject-checkbox"
                      checked={selectedSubjects.some(s => s.code === subject.code)}
                      onChange={(e) => handleSubjectSelection(subject.code, e.target.checked)}
                    />
                    {subject.code} - {subject.name}
                  </label>
                </div>
              ))}
            </div>
          </div>
        ) : semester ? (
          <p>No subjects found for this semester.</p>
        ) : null}

        {selectedSubjects.length > 0 && (
          <div className="schedule-section">
            <div className="section-titleCSS">
              <h3 className="section-title">
                Exam Schedule for Selected Subjects
                <span className="selection-count">{" "+selectedSubjects.length} selected</span>
              </h3>
            </div>

            <table className="schedule-table">
              <thead>
                <tr>
                  <th>Subject Code</th>
                  <th>Subject Name</th>
                  <th>Date</th>
                  <th>Session</th>
                </tr>
              </thead>
              <tbody>
                {selectedSubjects.map((subject) => (
                  <tr key={subject.code}>
                    <td>{subject.code}</td>
                    <td>{subject.name}</td>
                    <td>
                      <select
                        value={subjectSessions[subject.code]?.date || ""}
                        onChange={(e) => handleSessionChange(subject.code, "date", e.target.value)}
                        required
                      >
                        <option value="">Select Date</option>
                        {availableDates.map(date => (
                          <option key={date} value={date}>{date}</option>
                        ))}
                      </select>
                    </td>
                    <td>
                      <select
                        value={subjectSessions[subject.code]?.session || ""}
                        onChange={(e) => handleSessionChange(subject.code, "session", e.target.value)}
                        required
                      >
                        <option value="">Select Session</option>
                        <option value="Morning">Morning (10:00 AM - 11:30 AM)</option>
                        <option value="Afternoon">Afternoon (2:00 PM - 3:30 PM)</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <button
          type="submit"
          className="submit-button"
          disabled={selectedSubjects.length === 0 || loading}
        >
          {loading ? "Submitting..." : `Submit ${selectedSubjects.length} Exam Session(s)`}
        </button>
      </form>

      {/* Auto-generated Admit Card Section - Shows after form submission */}
      {showAdmitCardSection && (
        <div style={{
          marginTop: '40px',
          padding: '20px',
          border: '2px solid #4CAF50',
          borderRadius: '10px',
          backgroundColor: '#f9f9f9',
          animation: 'fadeIn 0.5s ease-in'
        }}>
          <h3 style={{ color: '#4CAF50', marginBottom: '20px' }}>
            🎫 Admit Card Generation - Ready!
          </h3>

          <div style={{ marginBottom: '15px' }}>
            <p style={{ fontWeight: 'bold', color: '#333' }}>
              Exam session submitted successfully! Generate admit cards for students:
            </p>
            <p style={{ color: '#666', fontSize: '14px' }}>
              Semester {semester} • {studentsForRecentExam.length} students found
            </p>
          </div>

          {admitCardLoading ? (
            <p>Loading students list...</p>
          ) : studentsForRecentExam.length > 0 ? (
            <div>
              {/* Students List */}
              <div style={{
                maxHeight: '300px',
                overflowY: 'auto',
                border: '1px solid #ddd',
                borderRadius: '4px',
                padding: '10px',
                marginBottom: '20px'
              }}>
                {studentsForRecentExam.map(student => (
                  <div key={student._id} style={{
                    padding: '10px',
                    borderBottom: '1px solid #eee',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between'
                  }}>
                    <div>
                      <strong>{student.student_name}</strong> - {student.reg_no} - {student.course} (Sem {student.sem})
                    </div>
                    <button
                      onClick={() => handleGenerateAdmitCard(student._id, student.student_name)}
                      disabled={admitCardLoading}
                      style={{
                        padding: '6px 12px',
                        backgroundColor: '#4CAF50',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        fontSize: '12px',
                        cursor: admitCardLoading ? 'not-allowed' : 'pointer'
                      }}
                    >
                      {admitCardLoading ? 'Generating...' : 'Download'}
                    </button>
                  </div>
                ))}
              </div>

              {/* Bulk Actions */}
              <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                <button
                  onClick={handleGenerateAllAdmitCards}
                  disabled={admitCardLoading}
                  style={{
                    padding: '12px 24px',
                    backgroundColor: '#2196F3',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px',
                    fontWeight: 'bold',
                    cursor: admitCardLoading ? 'not-allowed' : 'pointer'
                  }}
                >
                  {admitCardLoading ? 'Generating...' : `Generate All ${studentsForRecentExam.length} Admit Cards`}
                </button>
                <button
                  type="button"
                  onClick={clearPreviousSessions}
                  style={{
                    padding: '10px 20px',
                    backgroundColor: '#ff9800',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px',
                    marginRight: '10px'
                  }}
                >
                  Clear Previous Sessions
                </button>

                <button
                  onClick={() => setShowAdmitCardSection(false)}
                  style={{
                    padding: '12px 24px',
                    backgroundColor: '#f44336',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px'
                  }}
                >
                  Close
                </button>
              </div>
            </div>
          ) : (
            <p>No students found for this exam session.</p>
          )}
        </div>
      )}

      {/* Add some CSS animation */}
      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}

export default Dashboard;