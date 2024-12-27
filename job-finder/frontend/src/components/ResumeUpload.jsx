import React, { useState } from 'react';

const ResumeUpload = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [skills, setSkills] = useState([]);  // State to store extracted skills

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!file) {
            alert("Please upload a file.");
            return;
        }

        const formData = new FormData();
        formData.append('resume', file);

        try {
            const response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            console.log('Response from backend:', data);  // Debugging response

            if (data.message) {
                setMessage(data.message);
                setSkills(data.skills);  // Set skills from backend response
            } else {
                alert('Error uploading file');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error uploading file');
        }
    };

    return (
        <div>
            <h1>Upload Resume</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Upload Resume</button>
            </form>

            {message && <p>{message}</p>}

            {/* Display extracted skills */}
            {skills.length > 0 ? (
                <div>
                    <h3>Extracted Skills:</h3>
                    <ul>
                        {skills.map((skill, index) => (
                            <li key={index}>{skill}</li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p>No skills extracted yet.</p>
            )}
        </div>
    );
};

export default ResumeUpload;
