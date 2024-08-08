import  { useState } from 'react';
import { Link } from 'react-router-dom';
import './Collaboration.css';

const Collaboration = () => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState('');
  const [documents, setDocuments] = useState([]);
  const [documentInput, setDocumentInput] = useState('');

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (messageInput.trim()) {
      setMessages([...messages, messageInput]);
      setMessageInput('');
    }
  };

  const handleUploadDocument = (e) => {
    e.preventDefault();
    if (documentInput.trim()) {
      setDocuments([...documents, documentInput]);
      setDocumentInput('');
    }
  };

  return (
    <div className="collaboration-page">
      <header className="collaboration-header">
        <h1>Collaboration and Communication</h1>
        <p>Facilitate seamless collaboration among event organizers, team members, and participants.</p>
      </header>

      <section className="event-details">
        <h2>Event Details and Updates</h2>
        <p>Share the latest event details and updates with your team and participants.</p>
        {/* Implement actual event details sharing here */}
      </section>

      <section className="document-sharing">
        <h2>Document Sharing</h2>
        <form onSubmit={handleUploadDocument} className="document-form">
          <input
            type="text"
            placeholder="Enter document link or name"
            value={documentInput}
            onChange={(e) => setDocumentInput(e.target.value)}
            required
          />
          <button type="submit" className="button">Upload Document</button>
        </form>
        <div className="document-list">
          <h3>Shared Documents</h3>
          <ul>
            {documents.map((doc, index) => (
              <li key={index}>{doc}</li>
            ))}
          </ul>
        </div>
      </section>

      <section className="real-time-communication">
        <h2>Real-Time Communication</h2>
        <form onSubmit={handleSendMessage} className="message-form">
          <input
            type="text"
            placeholder="Type your message"
            value={messageInput}
            onChange={(e) => setMessageInput(e.target.value)}
            required
          />
          <button type="submit" className="button">Send Message</button>
        </form>
        <div className="message-list">
          <h3>Conversation</h3>
          <ul>
            {messages.map((message, index) => (
              <li key={index}>{message}</li>
            ))}
          </ul>
        </div>
      </section>

      <footer>
        <Link to="/home" className="button">Back to Home</Link>
      </footer>
    </div>
  );
};

export default Collaboration;
