import React, { useState } from "react";

const AdmitCardForm = ({ setAdmitCardData }) => {
  const [regNo, setRegNo] = useState("");
  const [name, setName] = useState("");
  const [subject, setSubject] = useState("");
  const [examDate, setExamDate] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Dummy data - backend se fetch karenge (Excel/Java)
    const studentData = {
      name: name || "Ayush Gupta",
      regNo: regNo || "RA241103003034",
      program: "B.Tech - CSE - CS/A",
      examDate: examDate,
      subject: subject
    };
    setAdmitCardData(studentData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Generate Admit Card</h3>
      <input
        type="text"
        placeholder="Registration Number"
        value={regNo}
        onChange={(e) => setRegNo(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Student Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="text"
        placeholder="Subject"
        value={subject}
        onChange={(e) => setSubject(e.target.value)}
        required
      />
      <input
        type="date"
        value={examDate}
        onChange={(e) => setExamDate(e.target.value)}
        required
      />
      <button type="submit">Preview Admit Card</button>
    </form>
  );
};

export default AdmitCardForm;
