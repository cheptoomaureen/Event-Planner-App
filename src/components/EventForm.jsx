import  { useState, useEffect } from 'react';
import axios from './api';  
import { useHistory } from 'react-router-dom';

const EventManager = () => {
  const [events, setEvents] = useState([]);
  const [event, setEvent] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const history = useHistory();

  const fetchEvents = async () => {
    try {
      const response = await axios.get('/events');
      setEvents(response.data);
    } catch (error) {
      console.error('Error fetching events', error);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  useEffect(() => {
    if (event) {
      setIsEditing(true);
    } else {
      setIsEditing(false);
    }
  }, [event]);

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/events/${id}`);
      fetchEvents();
    } catch (error) {
      console.error('Error deleting event', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const eventData = {
      title: e.target.title.value,
      date: e.target.date.value,
      location: e.target.location.value,
      description: e.target.description.value,
    };
    try {
      if (isEditing) {
        await axios.put(`/events/${event.id}`, eventData);
      } else {
        await axios.post('/events', eventData);
      }
      setEvent(null);
      fetchEvents();
      history.push('/');
    } catch (error) {
      console.error('Error creating/updating event', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h2>{isEditing ? 'Edit Event' : 'Create Event'}</h2>
        <div>
          <label>Title</label>
          <input
            type="text"
            name="title"
            defaultValue={event ? event.title : ''}
            required
          />
        </div>
        <div>
          <label>Date</label>
          <input
            type="date"
            name="date"
            defaultValue={event ? event.date : ''}
            required
          />
        </div>
        <div>
          <label>Location</label>
          <input
            type="text"
            name="location"
            defaultValue={event ? event.location : ''}
            required
          />
        </div>
        <div>
          <label>Description</label>
          <textarea
            name="description"
            defaultValue={event ? event.description : ''}
          />
        </div>
        <button type="submit">
          {isEditing ? 'Update Event' : 'Create Event'}
        </button>
      </form>

      <div>
        <h2>Events</h2>
        <ul>
          {events.map((event) => (
            <li key={event.id}>
              <h3>{event.title}</h3>
              <p>{event.date}</p>
              <p>{event.location}</p>
              <p>{event.description}</p>
              <button onClick={() => setEvent(event)}>Edit</button>
              <button onClick={() => handleDelete(event.id)}>Delete</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default EventManager;
