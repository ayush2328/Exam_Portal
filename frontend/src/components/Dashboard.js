import React, { useState, useEffect } from "react";

function Dashboard() {
  const [semester, setSemester] = useState("");
  const [branch, setBranch] = useState("Cyber Security");
  const [internalExam, setInternalExam] = useState("");
  const [monthYear, setMonthYear] = useState("");
  const [availableSubjects, setAvailableSubjects] = useState([]); // Subjects from backend
  const [selectedSubjects, setSelectedSubjects] = useState([]);   // Selected subjects for exam

  // Fetch subjects from backend when semester changes
  useEffect(() => {
    if (semester) {
      fetch(`http://localhost:8080/exambackend/GetSubjectsServlet?sem=${semester}`)
        .then(res => res.json())
        .then(data => {
          setAvailableSubjects(data);
          setSelectedSubjects([]); // Clear selected subjects when semester changes
        })
        .catch(err => console.error('Error fetching subjects:', err));
    } else {
      setAvailableSubjects([]);
      setSelectedSubjects([]);
    }
  }, [semester]);

  const handleSubjectSelection = (subjectCode, isSelected) => {
    if (isSelected) {
      // Add subject to selected list
      const subjectToAdd = availableSubjects.find(sub => sub.code === subjectCode);
      if (subjectToAdd) {
        setSelectedSubjects(prev => [...prev, subjectToAdd]);
      }
    } else {
      // Remove subject from selected list
      setSelectedSubjects(prev => prev.filter(sub => sub.code !== subjectCode));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (selectedSubjects.length === 0) {
      alert("Please select at least one subject!");
      return;
    }

    const payload = {
      semester: parseInt(semester),
      branch,
      internalExam,
      monthYear,
      subjects: selectedSubjects
    };

    try {
      const response = await fetch('http://localhost:8080/exambackend/AddExamSessionServlet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      console.log("Exam Session submitted successfully:", result);
      alert("Exam Session submitted successfully!");

      // Reset form
      setSemester("");
      setInternalExam("");
      setMonthYear("");
      setSelectedSubjects([]);

    } catch (error) {
      console.error('Error submitting exam session:', error);
      alert("Error submitting exam session. Please check console for details.");
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "900px", margin: "20px auto" }}>
      <h2 style={{ textAlign: "center" }}>Welcome Admin 🎉</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "15px" }}>
          <label>Semester: </label>
          <select value={semester} onChange={e => setSemester(e.target.value)} required>
            <option value="">Select Semester</option>
            <option value="1">1st</option>
            <option value="2">2nd</option>
            <option value="3">3rd</option>
            <option value="4">4th</option>
          </select>
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Branch: </label>
          <select value={branch} onChange={e => setBranch(e.target.value)} required>
            <option value="Cyber Security">Cyber Security</option>
            <option value="CSE">CSE</option>
            <option value="ECE">ECE</option>
          </select>
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Internal Exam: </label>
          <select value={internalExam} onChange={e => setInternalExam(e.target.value)} required>
            <option value="">Select Internal Exam</option>
            <option value="1st Internal">1st Internal</option>
            <option value="2nd Internal">2nd Internal</option>
          </select>
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label>Month & Year: </label>
          <input
            type="month"
            value={monthYear}
            onChange={e => setMonthYear(e.target.value)}
            required
          />
        </div>

        {availableSubjects.length > 0 && (
          <>
            <h3>Select Subjects for Exam</h3>
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
        )}

        {selectedSubjects.length > 0 && (
          <>
            <h3>Selected Subjects for Exam</h3>
            <ul>
              {selectedSubjects.map((subject, index) => (
                <li key={index}>
                  {subject.code} - {subject.name}
                </li>
              ))}
            </ul>
          </>
        )}

        <button type="submit" disabled={selectedSubjects.length === 0}>
          Submit Exam Session
        </button>
      </form>
    </div>
  );
}

export default Dashboard;