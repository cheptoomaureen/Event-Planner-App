import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Budget.css';

const Budget = () => {
  const [budgets, setBudgets] = useState([]);
  const [newBudget, setNewBudget] = useState({
    amount: '',
    description: '',
    event_id: ''
  });
  const [isEditing, setIsEditing] = useState(false);
  const [currentBudgetId, setCurrentBudgetId] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5555/expenses')
      .then(response => response.json())
      .then(data => setBudgets(data))
      .catch(error => console.error('Error fetching budgets:', error));
  }, []);

  const handleChange = (e) => {
    setNewBudget({ ...newBudget, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isEditing) {
      // Update the budget
      fetch(`http://localhost:5555/expenses/${currentBudgetId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newBudget)
      })
        .then(response => response.json())
        .then(updatedBudget => {
          setBudgets(budgets.map(budget => (budget.id === currentBudgetId ? updatedBudget : budget)));
          setIsEditing(false);
          setCurrentBudgetId(null);
          setNewBudget({
            amount: '',
            description: '',
            event_id: ''
          });
        })
        .catch(error => console.error('Error updating budget:', error));
    } else {
      // Create a new budget
      fetch('http://localhost:5555/expenses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newBudget)
      })
        .then(response => response.json())
        .then(data => {
          setBudgets([...budgets, data]);
          setNewBudget({
            amount: '',
            description: '',
            event_id: ''
          });
        })
        .catch(error => console.error('Error creating budget:', error));
    }
  };

  const handleEdit = (budget) => {
    setIsEditing(true);
    setCurrentBudgetId(budget.id);
    setNewBudget({
      amount: budget.amount,
      description: budget.description,
      event_id: budget.event_id
    });
  };

  const handleDelete = (id) => {
    fetch(`http://localhost:5555/expenses/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(() => {
        setBudgets(budgets.filter(budget => budget.id !== id));
      })
      .catch(error => console.error('Error deleting budget:', error));
  };

  return (
    <div className="budgets">
      <header className="budgets-header">
        <h1>Budget Planning and Expense Tracking</h1>
      </header>
      <section className="budgets-content">
        <div className="budget-list">
          {budgets.map(budget => (
            <div key={budget.id} className="budget-card">
              <h3>${budget.amount}</h3>
              <p>{budget.description}</p>
              <p>Event ID: {budget.event_id}</p>
              <div className="budget-actions">
                <button className="button" onClick={() => handleEdit(budget)}>Edit Budget</button>
                <button className="button" onClick={() => handleDelete(budget.id)}>Delete Budget</button>
              </div>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="budget-form">
          <input type="number" name="amount" placeholder="Amount" value={newBudget.amount} onChange={handleChange} required />
          <textarea name="description" placeholder="Description" value={newBudget.description} onChange={handleChange} required></textarea>
          <input type="text" name="event_id" placeholder="Event ID" value={newBudget.event_id} onChange={handleChange} required />
          <button type="submit" className="button">{isEditing ? 'Update Budget' : 'Create Budget'}</button>
        </form>
        <footer>
          <Link to="/home" className="button">Back to Home</Link>
        </footer>
      </section>
    </div>
  );
};

export default Budget;
