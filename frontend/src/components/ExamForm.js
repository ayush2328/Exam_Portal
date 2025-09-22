import React, { useState, useEffect } from 'react';
import { apiService } from "../services/api";

function ExamForm() {
    const [subjects, setSubjects] = useState([]);
    const [selectedSemester, setSelectedSemester] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [selectedSubjects, setSelectedSubjects] = useState([]);

    // Fetch subjects from backend
    useEffect(() => {
        const fetchSubjects = async () => {
            setLoading(true);
            setError('');
            try {
                const data = await apiService.getSubjects(selectedSemester);
                setSubjects(data);
            } catch (error) {
                setError('Failed to load subjects. Please try again.');
                console.error('Error fetching subjects:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchSubjects();
    }, [selectedSemester]);

    const handleSubjectSelect = (subjectCode) => {
        setSelectedSubjects(prev => {
            if (prev.includes(subjectCode)) {
                return prev.filter(code => code !== subjectCode);
            } else {
                return [...prev, subjectCode];
            }
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Handle form submission with selected subjects
        console.log('Selected subjects:', selectedSubjects);
        // You can add exam session creation logic here
    };

    return (
        <div className="exam-form">
            <h2>Exam Registration Form</h2>
            
            {error && <div className="error-message">{error}</div>}
            
            <form onSubmit={handleSubmit}>
                {/* Semester Selection */}
                <div className="form-group">
                    <label>Select Semester:</label>
                    <select 
                        value={selectedSemester} 
                        onChange={(e) => setSelectedSemester(e.target.value)}
                        className="form-select"
                    >
                        <option value="1">Semester 1</option>
                        <option value="2">Semester 2</option>
                        <option value="3">Semester 3</option>
                    </select>
                </div>

                {/* Subjects Selection */}
                <div className="subjects-section">
                    <h3>Select Subjects for Semester {selectedSemester}:</h3>
                    
                    {loading ? (
                        <p className="loading">Loading subjects...</p>
                    ) : (
                        <>
                            {subjects.length === 0 ? (
                                <p>No subjects found for this semester.</p>
                            ) : (
                                <div className="subjects-grid">
                                    {subjects.map(subject => (
                                        <div 
                                            key={subject.code} 
                                            className={`subject-card ${selectedSubjects.includes(subject.code) ? 'selected' : ''}`}
                                            onClick={() => handleSubjectSelect(subject.code)}
                                        >
                                            <input
                                                type="checkbox"
                                                checked={selectedSubjects.includes(subject.code)}
                                                onChange={() => handleSubjectSelect(subject.code)}
                                                style={{ marginRight: '10px' }}
                                            />
                                            <strong>{subject.code}</strong>
                                            <br />
                                            {subject.name}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </>
                    )}
                </div>

                {/* Submit Button */}
                {selectedSubjects.length > 0 && (
                    <button type="submit" className="submit-btn">
                        Register for {selectedSubjects.length} Subject(s)
                    </button>
                )}

                {/* Selection Summary */}
                {selectedSubjects.length > 0 && (
                    <div className="selection-summary">
                        <h4>Selected Subjects ({selectedSubjects.length}):</h4>
                        <ul>
                            {selectedSubjects.map(code => {
                                const subject = subjects.find(s => s.code === code);
                                return <li key={code}>{subject?.code} - {subject?.name}</li>;
                            })}
                        </ul>
                    </div>
                )}
            </form>

            {/* Subject Count */}
            {!loading && subjects.length > 0 && (
                <p className="subject-count">
                    Total {subjects.length} subject(s) available
                </p>
            )}
        </div>
    );
}

export default ExamForm;