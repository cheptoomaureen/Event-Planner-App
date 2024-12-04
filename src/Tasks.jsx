import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Tasks.css';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    deadline: '',
    priority: '',
    status: '',
    event_id: '',
    assigned_to: ''
  });
  const [isEditing, setIsEditing] = useState(false);
  const [currentTaskId, setCurrentTaskId] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5555/tasks')
      .then(response => response.json())
      .then(data => setTasks(data))
      .catch(error => console.error('Error fetching tasks:', error));
  }, []);

  const handleChange = (e) => {
    setNewTask({ ...newTask, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isEditing) {
      // Update the task
      fetch(`http://localhost:5555/tasks/${currentTaskId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTask)
      })
        .then(response => response.json())
        .then(updatedTask => {
          setTasks(tasks.map(task => (task.id === currentTaskId ? updatedTask : task)));
          setIsEditing(false);
          setCurrentTaskId(null);
          setNewTask({
            title: '',
            description: '',
            deadline: '',
            priority: '',
            status: '',
            event_id: '',
            assigned_to: ''
          });
        })
        .catch(error => console.error('Error updating task:', error));
    } else {
      // Create a new task
      fetch('http://localhost:5555/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTask)
      })
        .then(response => response.json())
        .then(data => {
          setTasks([...tasks, data]);
          setNewTask({
            title: '',
            description: '',
            deadline: '',
            priority: '',
            status: '',
            event_id: '',
            assigned_to: ''
          });
        })
        .catch(error => console.error('Error creating task:', error));
    }
  };

  const handleEdit = (task) => {
    setIsEditing(true);
    setCurrentTaskId(task.id);
    setNewTask({
      title: task.title,
      description: task.description,
      deadline: task.deadline,
      priority: task.priority,
      status: task.status,
      event_id: task.event_id,
      assigned_to: task.assigned_to
    });
  };

  const handleDelete = (id) => {
    fetch(`http://localhost:5555/tasks/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(() => {
        setTasks(tasks.filter(task => task.id !== id));
      })
      .catch(error => console.error('Error deleting task:', error));
  };

  return (
    <div className="tasks">
      <header className="tasks-header">
        <h1>Task Management</h1>
      </header>
      
      <section className="tasks-content">
        <form onSubmit={handleSubmit} className="task-form">
          <input type="text" name="title" placeholder="Task Title" value={newTask.title} onChange={handleChange} required />
          <textarea name="description" placeholder="Description" value={newTask.description} onChange={handleChange} required></textarea>
          <input type="date" name="deadline" placeholder="Deadline" value={newTask.deadline} onChange={handleChange} required />
          <input type="text" name="priority" placeholder="Priority" value={newTask.priority} onChange={handleChange} required />
          <input type="text" name="status" placeholder="Status" value={newTask.status} onChange={handleChange} required />
          <input type="text" name="event_id" placeholder="Event ID" value={newTask.event_id} onChange={handleChange} required />
          <input type="text" name="assigned_to" placeholder="Assigned To" value={newTask.assigned_to} onChange={handleChange} required />
          <button type="submit" className="button">{isEditing ? 'Update Task' : 'Create Task'}</button>
        </form>
        <div className="task-list">
          {tasks.map(task => (
            <div key={task.id} className="task-card">
              <h3>{task.title}</h3>
              <p>{task.description}</p>
              <p>{task.deadline}</p>
              <p>{task.priority}</p>
              <p>{task.status}</p>
              <p>Event ID: {task.event_id}</p>
              <p>Assigned To: {task.assigned_to}</p>
              <div className="task-actions">
                <button className="button" onClick={() => handleEdit(task)}>Edit </button>
                <button className="button" onClick={() => handleDelete(task.id)}>Delete </button>
              </div>
            </div>
          ))}
        </div>
        <footer>
          <Link to="/home" className="button">Back to Home</Link>
        </footer>
      </section>
    </div>
  );
  
};

export default Tasks;
