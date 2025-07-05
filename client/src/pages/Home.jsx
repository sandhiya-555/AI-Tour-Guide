import React, { useState } from 'react';
import UploadForm from '../components/UploadForm';

function Home() {
  const [answer, setAnswer] = useState('');
  const [fact, setFact] = useState('');
  const [link, setLink] = useState('');
  const [loading, setLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);

  const handleFormSubmit = async ({ image, question }) => {
    setAnswer('');
    setFact('');
    setLink('');
    setLoading(true);
    setImagePreview(URL.createObjectURL(image)); // show preview

    const formData = new FormData();
    formData.append('image', image);
    formData.append('question', question);

    try {
      const response = await fetch('http://localhost:5000/api/vqa', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error("Failed to get response from backend.");
      }

      const data = await response.json();
      setAnswer(data.answer || "No answer received.");
      setFact(data.fact || "");
      setLink(data.link || "");
    } catch (error) {
      console.error("Error:", error);
      setAnswer("Error communicating with AI backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: 'auto', padding: '1rem' }}>
      <UploadForm onSubmit={handleFormSubmit} />

      {imagePreview && (
        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <strong>Uploaded Image:</strong><br />
          <img
            src={imagePreview}
            alt="Uploaded preview"
            style={{ maxWidth: '100%', height: 'auto', borderRadius: '10px', marginTop: '10px' }}
          />
        </div>
      )}

      {loading && (
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <div className="spinner" />
          <p>Processing your request...</p>
        </div>
      )}

      {!loading && answer && (
        <>
          <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
            <strong>🔤 Answer:</strong> {answer}
          </div>
          {fact && (
            <div style={{ marginTop: '10px', padding: '10px', background: '#f1f8e9', border: '1px solid #c5e1a5' }}>
              <strong>🧠 Cultural Fact:</strong> {fact}
            </div>
          )}
          {link && (
            <p style={{ marginTop: '10px' }}>
              🌐 <a href={link} target="_blank" rel="noopener noreferrer">
                Learn more on Wikipedia
              </a>
            </p>
          )}
        </>
      )}
    </div>
  );
}

export default Home;
