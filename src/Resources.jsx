import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Resources.css';

const Resources = () => {
  const [resources, setResources] = useState([]);
  const [newResource, setNewResource] = useState({
    name: '',
    type: '',
    status: 'available',  // Default status to 'available'
    event_id: '',
    reserved_by: '',
    cost: 0,  // Add a cost field for budget management
    availability: 'available'  // Track resource availability
  });
  const [isEditing, setIsEditing] = useState(false);
  const [currentResourceId, setCurrentResourceId] = useState(null);
  const [budget, setBudget] = useState(1000);  // Set a reasonable default budget

  useEffect(() => {
    fetch('http://localhost:5555/resources')
      .then(response => response.json())
      .then(data => setResources(data))
      .catch(error => console.error('Error fetching resources:', error));
  }, []);

  const handleChange = (e) => {
    setNewResource({ ...newResource, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Only check budget if it's set and greater than zero
    if (budget > 0 && newResource.cost > budget) {
      alert('This resource exceeds the event budget.');
      return;
    }

    if (isEditing) {
      // Update the resource
      fetch(`http://localhost:5555/resources/${currentResourceId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newResource)
      })
        .then(response => response.json())
        .then(updatedResource => {
          setResources(resources.map(resource => (resource.id === currentResourceId ? updatedResource : resource)));
          setIsEditing(false);
          setCurrentResourceId(null);
          setNewResource({
            name: '',
            type: '',
            status: 'available',
            event_id: '',
            reserved_by: '',
            cost: 0,
            availability: 'available'
          });
        })
        .catch(error => console.error('Error updating resource:', error));
    } else {
      // Create a new resource
      fetch('http://localhost:5555/resources', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newResource)
      })
        .then(response => response.json())
        .then(data => {
          setResources([...resources, data]);
          setNewResource({
            name: '',
            type: '',
            status: 'available',
            event_id: '',
            reserved_by: '',
            cost: 0,
            availability: 'available'
          });
        })
        .catch(error => console.error('Error creating resource:', error));
    }
  };

  const handleEdit = (resource) => {
    setIsEditing(true);
    setCurrentResourceId(resource.id);
    setNewResource({
      name: resource.name,
      type: resource.type,
      status: resource.status,
      event_id: resource.event_id,
      reserved_by: resource.reserved_by,
      cost: resource.cost,
      availability: resource.availability
    });
  };

  const handleDelete = (id) => {
    fetch(`http://localhost:5555/resources/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(() => {
        setResources(resources.filter(resource => resource.id !== id));
      })
      .catch(error => console.error('Error deleting resource:', error));
  };

  const handleReserve = (id) => {
    const updatedResources = resources.map(resource => {
      if (resource.id === id && resource.availability === 'available') {
        resource.availability = 'reserved';
        resource.status = 'reserved';
      }
      return resource;
    });
    setResources(updatedResources);
  };

  return (
    <div className="resources">
      <header className="resources-header">
        <h1>Resource Management</h1>
      </header>
      
      <section className="resources-content">
        <form onSubmit={handleSubmit} className="resource-form">
          <input type="text" name="name" placeholder="Resource Name" value={newResource.name} onChange={handleChange} required />
          <input type="text" name="type" placeholder="Type" value={newResource.type} onChange={handleChange} required />
          <input type="text" name="status" placeholder="Status" value={newResource.status} onChange={handleChange} required />
          <input type="text" name="event_id" placeholder="Event ID" value={newResource.event_id} onChange={handleChange} required />
          <input type="text" name="reserved_by" placeholder="Reserved By" value={newResource.reserved_by} onChange={handleChange} />
          <input type="number" name="cost" placeholder="Cost" value={newResource.cost} onChange={handleChange} required />
          <button type="submit" className="button">{isEditing ? 'Update Resource' : 'Create Resource'}</button>
        </form>

        <div className="resource-list">
          {resources.map(resource => (
            <div key={resource.id} className="resource-card">
              <h3>{resource.name}</h3>
              <p>Type: {resource.type}</p>
              <p>Status: {resource.status}</p>
              <p>Event ID: {resource.event_id}</p>
              <p>Reserved By: {resource.reserved_by}</p>
              <p>Cost: ${resource.cost}</p>
              <p>Availability: {resource.availability}</p>
              <div className="resource-actions">
                <button className="button" onClick={() => handleEdit(resource)}>Edit Resource</button>
                <button className="button" onClick={() => handleDelete(resource.id)}>Delete Resource</button>
                {resource.availability === 'available' && (
                  <button className="button" onClick={() => handleReserve(resource.id)}>Reserve Resource</button>
                )}
              </div>
            </div>
          ))}
        </div>

        <footer>
          <input 
            type="number" 
            name="budget" 
            placeholder="Set Event Budget" 
            value={budget} 
            onChange={(e) => setBudget(Number(e.target.value))} 
            required 
          />
          <Link to="/home" className="button">Back to Home</Link>
        </footer>
      </section>
    </div>
  );
};

export default Resources;
