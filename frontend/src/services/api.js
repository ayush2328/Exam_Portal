// Updated api.js with data transformation
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

console.log('🔧 API Configuration:');
console.log('API_BASE_URL:', API_BASE_URL);

export const apiService = {
  getSubjects: async (semester) => {
    try {
      const url = `${API_BASE_URL}/subjects/?sem=${semester}`;
      console.log('📞 Calling getSubjects:', url);
      
      const response = await fetch(url);
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('✅ Raw API Response:', data);
      
      // Transform data to match frontend expectations
      const transformedSubjects = data.subjects ? data.subjects.map(subject => ({
        code: subject.subject_code,    // Map subject_code → code
        name: subject.subject_name,    // Map subject_name → name
        semester: subject.sem,         // Map sem → semester
        id: subject._id || subject.id  // Keep ID for reference
      })) : [];
      
      console.log('🔄 Transformed subjects:', transformedSubjects);
      return transformedSubjects;
    } catch (error) {
      console.error('❌ Error in getSubjects:', error);
      throw error;
    }
  },

  // Health check to verify connection
  healthCheck: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health/`);
      const data = await response.json();
      console.log('🏥 Backend Health:', data);
      return data;
    } catch (error) {
      console.error('❌ Health check failed:', error);
      throw error;
    }
  },

  addExamSession: async (examData) => {
    try {
      const params = new URLSearchParams({
        subject_code: examData.subjectCode,
        exam_date: examData.examDate,
        exam_time: examData.examTime,
        sem: examData.semester.toString()
      });
      
      const url = `${API_BASE_URL}/exam-sessions/?${params}`;
      console.log('📤 Adding exam session:', url);
      
      const response = await fetch(url, {
        method: 'POST'
      });
      
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      
      const result = await response.json();
      console.log('✅ Exam session added:', result);
      return result;
    } catch (error) {
      console.error('❌ Error adding exam session:', error);
      throw error;
    }
  }
};