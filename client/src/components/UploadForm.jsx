import React, { useState } from 'react';

function UploadForm({ onSubmit }) {
  const [image, setImage] = useState(null);
  const [question, setQuestion] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (image && question) {
      onSubmit({ image, question });
    } else {
      alert("Please upload an image and type a question.");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        alignItems: 'center',
        padding: '1rem',
        border: '1px solid #ddd',
        borderRadius: '10px',
        backgroundColor: '#f5f5f5',
      }}
    >
      <h2 style={{ marginBottom: '0.5rem' }}>📸 Upload an Image & Ask a Question</h2>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImage(e.target.files[0])}
        required
        style={{
          padding: '0.5rem',
          backgroundColor: '#fff',
          border: '1px solid #ccc',
          borderRadius: '5px',
          width: '100%',
          maxWidth: '400px',
        }}
      />

      <input
        type="text"
        placeholder="Type your question here..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        required
        style={{
          padding: '0.5rem',
          border: '1px solid #ccc',
          borderRadius: '5px',
          width: '100%',
          maxWidth: '400px',
        }}
      />

      <button
        type="submit"
        style={{
          backgroundColor: '#1976d2',
          color: '#fff',
          border: 'none',
          padding: '0.7rem 1.5rem',
          borderRadius: '5px',
          cursor: 'pointer',
        }}
      >
        Ask AI
      </button>
    </form>
  );
}

export default UploadForm;
