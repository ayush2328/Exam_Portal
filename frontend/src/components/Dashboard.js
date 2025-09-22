import React, { useState, useEffect } from "react";
import { apiService } from "../services/api";  // ✅ CORRECT PATH

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

  // Generate years (current year and next 2 years)
  const years = Array.from({ length: 3 }, (_, i) => new Date().getFullYear() + i);

  // Months list
  const months = [
    { value: "01", name: "January" },
    { value: "02", name: "February" },
    { value: "03", name: "March" },
    { value: "04", name: "April" },
    { value: "05", name: "May" },
    { value: "06", name: "June" },
    { value: "07", name: "July" },
    { value: "08", name: "August" },
    { value: "09", name: "September" },
    { value: "10", name: "October" },
    { value: "11", name: "November" },
    { value: "12", name: "December" }
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

  // Fetch subjects from backend when semester changes - USING CORRECT API
  useEffect(() => {
    if (semester) {
      setLoading(true);
      setError("");

      // USING API SERVICE INSTEAD OF DIRECT FETCH
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

    // Validate all subjects have date and session
    const incompleteSubjects = selectedSubjects.filter(subject =>
      !subjectSessions[subject.code]?.date || !subjectSessions[subject.code]?.session
    );

    if (incompleteSubjects.length > 0) {
      alert("Please select date and session for all subjects!");
      return;
    }

    // For each selected subject, submit individually
    try {
      const submissionPromises = selectedSubjects.map(async (subject) => {
        const examData = {
          subjectCode: subject.code,
          examDate: `${year}-${month}-${subjectSessions[subject.code].date.toString().padStart(2, '0')}`,
          examTime: subjectSessions[subject.code].session,
          semester: parseInt(semester)
        };

        return await apiService.addExamSession(examData);
      });

      // Wait for all submissions to complete
      const results = await Promise.all(submissionPromises);
      console.log("All exam sessions submitted successfully:", results);
      alert(`Successfully submitted ${selectedSubjects.length} exam session(s)!`);

      // Reset form
      setSemester("");
      setInternalExam("");
      setYear(new Date().getFullYear());
      setMonth("");
      setSelectedSubjects([]);
      setSubjectSessions({});

    } catch (error) {
      console.error('Error submitting exam session:', error);
      alert("Error submitting exam session. Please check console for details.");
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "1000px", margin: "20px auto" }}>
      <h2 style={{ textAlign: "center" }}>Welcome Admin 🎉</h2>

      {error && <div style={{ color: "red", textAlign: "center", marginBottom: "15px" }}>{error}</div>}

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "15px", display: "flex", gap: "20px", flexWrap: "wrap" }}>
          <div>
            <label>Semester: </label>
            <select value={semester} onChange={e => setSemester(e.target.value)} required>
              <option value="">Select Semester</option>
              <option value="1">1st</option>
              <option value="2">2nd</option>
              <option value="3">3rd</option>
              <option value="4">4th</option>
            </select>
          </div>

          <div>
            <label>Branch: </label>
            <select value={branch} onChange={e => setBranch(e.target.value)} required>
              <option value="Cyber Security">Cyber Security</option>
              <option value="CSE">CSE</option>
              <option value="ECE">ECE</option>
            </select>
          </div>

          <div>
            <label>Internal Exam: </label>
            <select value={internalExam} onChange={e => setInternalExam(e.target.value)} required>
              <option value="">Select Internal Exam</option>
              <option value="1st Internal">1st Internal</option>
              <option value="2nd Internal">2nd Internal</option>
            </select>
          </div>

          <div>
            <label>Year: </label>
            <select value={year} onChange={e => setYear(e.target.value)} required>
              {years.map(y => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          </div>

          <div>
            <label>Month: </label>
            <select value={month} onChange={e => setMonth(e.target.value)} required>
              <option value="">Select Month</option>
              {months.map(m => (
                <option key={m.value} value={m.value}>{m.name}</option>
              ))}
            </select>
          </div>
        </div>

        {loading ? (
          <p>Loading subjects...</p>
        ) : availableSubjects.length > 0 ? (
          <>
            <h3>Select Subjects for Exam ({availableSubjects.length} subjects available)</h3>
            <div style={{ marginBottom: "20px", maxHeight: "300px", overflowY: "auto", border: "1px solid #ccc", padding: "10px" }}>
              {availableSubjects.map((subject) => (
                <div key={subject.code} style={{ marginBottom: "10px" }}>
                  <label>
                    <input
                      type="checkbox"
                      checked={selectedSubjects.some(s => s.code === subject.code)}
                      onChange={(e) => handleSubjectSelection(subject.code, e.target.checked)}
                      style={{ marginRight: "10px" }}
                    />
                    {subject.code} - {subject.name}
                  </label>
                </div>
              ))}
            </div>
          </>
        ) : semester ? (
          <p>No subjects found for this semester.</p>
        ) : null}

        {selectedSubjects.length > 0 && (
          <>
            <h3>Exam Schedule for Selected Subjects ({selectedSubjects.length} selected)</h3>
            <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: "20px" }}>
              <thead>
                <tr style={{ backgroundColor: "#f5f5f5" }}>
                  <th style={{ border: "1px solid #ddd", padding: "8px" }}>Subject Code</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px" }}>Subject Name</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px" }}>Date</th>
                  <th style={{ border: "1px solid #ddd", padding: "8px" }}>Session</th>
                </tr>
              </thead>
              <tbody>
                {selectedSubjects.map((subject) => (
                  <tr key={subject.code}>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>{subject.code}</td>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>{subject.name}</td>
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>
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
                    <td style={{ border: "1px solid #ddd", padding: "8px" }}>
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
          </>
        )}

        <button
          type="submit"
          disabled={selectedSubjects.length === 0 || loading}
          style={{
            padding: "10px 20px",
            backgroundColor: selectedSubjects.length === 0 || loading ? "#ccc" : "#007bff",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: selectedSubjects.length === 0 || loading ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "Submitting..." : `Submit ${selectedSubjects.length} Exam Session(s)`}
        </button>
      </form>
    </div>
  );
}

export default Dashboard;