// API service functions
const API_BASE = 'http://localhost:8080/exambackend';

export const apiService = {
  // Get subjects for a semester
  getSubjects: async (semester) => {
    const response = await fetch(`${API_BASE}/GetSubjectsServlet?sem=${semester}`);
    return await response.json();
  },

  // Add exam session
  addExamSession: async (examData) => {
    const response = await fetch(`${API_BASE}/AddExamSessionServlet`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(examData)
    });
    return await response.json();
  }
};