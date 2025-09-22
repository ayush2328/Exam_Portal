const submitExamSession = async (examData) => {
  console.log('Submitting exam data:', examData);
  
  try {
    const response = await fetch('http://localhost:8080/exambackend/AddExamSessionServlet', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(examData)
    });
    
    console.log('Response status:', response.status);
    const result = await response.json();
    console.log('Backend response:', result);
    return result;
    
  } catch (error) {
    console.error('Error submitting exam:', error);
    throw error;
  }
};