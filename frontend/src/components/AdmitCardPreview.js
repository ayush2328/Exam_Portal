import React from "react";
import { jsPDF } from "jspdf";

const AdmitCardPreview = ({ admitCardData }) => {
  if (!admitCardData) return null;

  const downloadPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("Internal Examinations - I, September 2025", 20, 20);
    doc.text(`Name: ${admitCardData.name}`, 20, 40);
    doc.text(`Registration No: ${admitCardData.regNo}`, 20, 50);
    doc.text(`Program: ${admitCardData.program}`, 20, 60);
    doc.text(`Subject: ${admitCardData.subject}`, 20, 70);
    doc.text(`Exam Date: ${admitCardData.examDate}`, 20, 80);
    doc.save("AdmitCard.pdf");
  };

  return (
    <div style={{ border: "1px solid black", padding: "20px", marginTop: "20px" }}>
      <h2>Admit Card Preview</h2>
      <p><b>Name:</b> {admitCardData.name}</p>
      <p><b>Reg No:</b> {admitCardData.regNo}</p>
      <p><b>Program:</b> {admitCardData.program}</p>
      <p><b>Subject:</b> {admitCardData.subject}</p>
      <p><b>Exam Date:</b> {admitCardData.examDate}</p>
      <button onClick={downloadPDF}>Download PDF</button>
    </div>
  );
};

export default AdmitCardPreview;
