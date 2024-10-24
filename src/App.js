import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');

  const onDrop = useCallback((acceptedFiles) => {
    const formData = new FormData();
    formData.append('file', acceptedFiles[0]);

    axios.post('http://localhost:5001/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(response => {
      setMessage(response.data.message);  // Display the success message
    })
    .catch(error => {
      console.error(error);
      setMessage('File upload failed.');
    });
  }, []);

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div className="App">
      <h1>Gym Workout Suggestion</h1>
      <p>Upload your photo to get workout suggestions!</p>

      <div {...getRootProps()} style={{ border: '2px dashed #aaa', padding: '20px', textAlign: 'center' }}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop a photo here, or click to select one</p>
      </div>

      {message && <p>{message}</p>}  {/* Display the message */}
    </div>
  );
}

export default App;
