// API service functions
const API_BASE = 'http://localhost:8080/ExamBackend';

export const apiService = {
  // Get subjects for a semester
  getSubjects: async (semester) => {
    try {
      const response = await fetch(`${API_BASE}/getSubjects?sem=${semester}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching subjects:', error);
      throw error;
    }
  },

  // Add exam session
  addExamSession: async (examData) => {
    try {
      // Convert to URL-encoded format as your servlet expects
      const formData = new URLSearchParams();
      formData.append('subjectCode', examData.subjectCode);
      formData.append('examDate', examData.examDate);
      formData.append('examTime', examData.examTime);
      formData.append('semester', examData.semester);

      const response = await fetch(`${API_BASE}/addExamSession`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error adding exam session:', error);
      throw error;
    }
  }
};