// import React from "react";

// function Dashboard() {
//   return (
//     <div style={{ textAlign: "center", marginTop: "100px" }}>
//       <h2>Welcome Admin 🎉</h2>
    
//     </div>
//   );
// }

// export default Dashboard;



import React, { useState, useEffect } from "react";

function Dashboard() {
  const [semester, setSemester] = useState("");
  const [branch, setBranch] = useState("Cyber Security");
  const [internalExam, setInternalExam] = useState("");
  const [monthYear, setMonthYear] = useState("");
  const [subjects, setSubjects] = useState([]);

  // Fetch subjects from backend when semester changes
  useEffect(() => {
    if (semester) {
      fetch(`/api/subjects?sem=${semester}`)
        .then(res => res.json())
        .then(data => setSubjects(data))
        .catch(err => console.error(err));
    } else {
      setSubjects([]);
    }
  }, [semester]);

  const handleSubjectChange = (index, field, value) => {
    const updatedSubjects = [...subjects];
    updatedSubjects[index][field] = value;
    setSubjects(updatedSubjects);
  };

  const addSubjectRow = () => {
    setSubjects([...subjects, { code: "", name: "" }]);
  };

  const removeSubjectRow = (index) => {
    const updatedSubjects = subjects.filter((_, i) => i !== index);
    setSubjects(updatedSubjects);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Future backend API call
    const payload = {
      semester,
      branch,
      internalExam,
      monthYear,
      subjects
    };
    console.log("Submitting Exam Session:", payload);
    alert("Exam Session submitted! (Backend integration pending)");
  };

  return (
    <div style={{ padding: "20px", maxWidth: "900px", margin: "20px auto" }}>
      <h2 style={{ textAlign: "center" }}>Welcome Admin 🎉</h2>
      <form onSubmit={handleSubmit}>
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
          <label>Month & Year: </label>
          <input type="month" value={monthYear} onChange={e => setMonthYear(e.target.value)} required />
        </div>

        <h3>Subject List</h3>
        <table style={{ width: "100%", marginBottom: "20px", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ border: "1px solid black" }}>Subject Code</th>
              <th style={{ border: "1px solid black" }}>Subject Name</th>
              <th style={{ border: "1px solid black" }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {subjects.map((sub, index) => (
              <tr key={index}>
                <td style={{ border: "1px solid black" }}>
                  <input
                    type="text"
                    value={sub.code}
                    onChange={e => handleSubjectChange(index, "code", e.target.value)}
                    required
                  />
                </td>
                <td style={{ border: "1px solid black" }}>
                  <input
                    type="text"
                    value={sub.name}
                    onChange={e => handleSubjectChange(index, "name", e.target.value)}
                    required
                  />
                </td>
                <td style={{ border: "1px solid black" }}>
                  <button type="button" onClick={() => removeSubjectRow(index)}>Remove</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <button type="button" onClick={addSubjectRow} style={{ marginRight: "10px" }}>Add Subject</button>
        <button type="submit">Submit Exam Session</button>
      </form>
    </div>
  );
}

export default Dashboard;
