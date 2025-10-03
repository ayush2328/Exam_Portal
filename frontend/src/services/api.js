// API service functions - Support both local and production
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://exam-portal-backend-rmov.onrender.com';

// Just append endpoint - your servlets are mapped directly in web.xml to /getSubjects etc.
const buildApiUrl = (endpoint) => `${API_BASE_URL}${endpoint}`;

export const apiService = {
  getSubjects: async (semester) => {
    try {
      const response = await fetch(buildApiUrl(`/getSubjects?sem=${semester}`));
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching subjects:', error);
      throw error;
    }
  },

  addExamSession: async (examData) => {
    try {
      const formData = new URLSearchParams();
      formData.append('subjectCode', examData.subjectCode);
      formData.append('examDate', examData.examDate);
      formData.append('examTime', examData.examTime);
      formData.append('semester', examData.semester);

      const response = await fetch(buildApiUrl('/addExamSession'), {
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
