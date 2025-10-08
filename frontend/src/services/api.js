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
  },

  // Get all exam sessions
  getExamSessions: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/exam-sessions/`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      return data.sessions || [];
    } catch (error) {
      console.error('❌ Error fetching exam sessions:', error);
      throw error;
    }
  },

  // Get students by exam session
  getStudentsByExamSession: async (examSessionId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/students-by-exam/${examSessionId}`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error('❌ Error fetching students by exam:', error);
      throw error;
    }
  },

  // Admit card generation function
  generateAdmitCard: async (studentId) => {
    try {
      console.log('🎫 Generating admit card for student:', studentId);

      const response = await fetch(`${API_BASE_URL}/generate-admit-card/${studentId}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Get the PDF blob
      const pdfBlob = await response.blob();

      // Create download link
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `admit_card_${studentId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      console.log('✅ Admit card downloaded successfully');
      return { success: true, message: 'Admit card downloaded' };
    } catch (error) {
      console.error('❌ Error generating admit card:', error);
      throw error;
    }
  },

  // Bulk admit card generation
  generateBulkAdmitCards: async (studentIds) => {
    try {
      console.log('🎫 Generating bulk admit cards for:', studentIds.length, 'students');
      
      // Generate admit cards one by one (for now)
      for (let i = 0; i < studentIds.length; i++) {
        const studentId = studentIds[i];
        console.log(`Generating admit card ${i + 1}/${studentIds.length} for student:`, studentId);
        
        const response = await fetch(`${API_BASE_URL}/generate-admit-card/${studentId}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const pdfBlob = await response.blob();
        const url = window.URL.createObjectURL(pdfBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `admit_card_${studentId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        // Small delay to avoid overwhelming the browser
        await new Promise(resolve => setTimeout(resolve, 500));
      }
      
      console.log('✅ All admit cards generated successfully');
      return { success: true, message: `Generated ${studentIds.length} admit cards` };
    } catch (error) {
      console.error('❌ Error generating bulk admit cards:', error);
      throw error;
    }
  }
};