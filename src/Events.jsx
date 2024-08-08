import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Events.css';

const Events = () => {
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState({
    title: '',
    date: '',
    time: '',
    location: '',
    description: '',
    participants: ''
  });
  const [isEditing, setIsEditing] = useState(false);
  const [currentEventId, setCurrentEventId] = useState(null);

  useEffect(() => {
    // Fetch all events when the component loads
    const token = localStorage.getItem('token'); // Retrieve the JWT token from localStorage
    fetch('http://localhost:5555/events', {
      headers: {
        'Authorization': `Bearer ${token}` // Include token in the request headers
      }
    })
      .then(response => response.json())
      .then(data => setEvents(data))
      .catch(error => console.error('Error fetching events:', error));
  }, []);

  const handleChange = (e) => {
    setNewEvent({ ...newEvent, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token'); // Retrieve the JWT token from localStorage

    if (isEditing) {
      // Update the event
      fetch(`http://localhost:5555/events/${currentEventId}`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // Include token in the request headers
        },
        body: JSON.stringify(newEvent)
      })
        .then(response => response.json())
        .then(updatedEvent => {
          setEvents(events.map(event => (event.id === currentEventId ? updatedEvent : event)));
          setIsEditing(false);
          setCurrentEventId(null);
          setNewEvent({
            title: '',
            date: '',
            time: '',
            location: '',
            description: '',
            participants: ''
          });
        })
        .catch(error => console.error('Error updating event:', error));
    } else {
      // Create a new event
      fetch('http://localhost:5555/events', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` // Include token in the request headers
        },
        body: JSON.stringify(newEvent)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to create event');
          }
          return response.json();
        })
        .then(createdEvent => {
          setEvents([...events, createdEvent]);
          setNewEvent({
            title: '',
            date: '',
            time: '',
            location: '',
            description: '',
            participants: ''
          });
        })
        .catch(error => console.error('Error creating event:', error));
    }
  };

  const handleEdit = (event) => {
    setIsEditing(true);
    setCurrentEventId(event.id);
    setNewEvent({
      title: event.title,
      date: event.date,
      time: event.time,
      location: event.location,
      description: event.description,
      participants: event.participants
    });
  };

  const handleDelete = (id) => {
    const token = localStorage.getItem('token'); // Retrieve the JWT token from localStorage

    fetch(`http://localhost:5555/events/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}` // Include token in the request headers
      }
    })
      .then(() => {
        setEvents(events.filter(event => event.id !== id));
      })
      .catch(error => console.error('Error deleting event:', error));
  };

  return (
    <div className="events">
      <header className="events-header">
        <h1>Event Management</h1>
      </header>
      <section className="events-content">
        <div className="event-list">
          {events.map(event => (
            <div key={event.id} className="event-card">
              <h3>{event.title}</h3>
              <p>{event.date} {event.time}</p>
              <p>{event.location}</p>
              <p>{event.description}</p>
              <p>{event.participants}</p>
              <div className="event-actions">
                <button className="button" onClick={() => handleEdit(event)}>Edit</button>
                <button className="button" onClick={() => handleDelete(event.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="event-form">
          <input type="text" name="title" placeholder="Event Title" value={newEvent.title} onChange={handleChange} required />
          <input type="date" name="date" placeholder="Date" value={newEvent.date} onChange={handleChange} required />
          <input type="time" name="time" placeholder="Time" value={newEvent.time} onChange={handleChange} required />
          <input type="text" name="location" placeholder="Location" value={newEvent.location} onChange={handleChange} required />
          <textarea name="description" placeholder="Description" value={newEvent.description} onChange={handleChange} required></textarea>
          <input type="text" name="participants" placeholder="Participants" value={newEvent.participants} onChange={handleChange} required />
          <button type="submit" className="button">{isEditing ? 'Update Event' : 'Create Event'}</button>
        </form>
        <Link to="/home" className="button">Back to Home</Link>
      </section>
    </div>
  );
};

export default Events;
