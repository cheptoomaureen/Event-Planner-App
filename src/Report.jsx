import  { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import './Report.css';

const Report = () => {
  const [expenses, setExpenses] = useState([]);

  useEffect(() => {
    // Fetch the expense data
    fetch('http://localhost:5555/expenses')
      .then(response => response.json())
      .then(data => setExpenses(data))
      .catch(error => console.error('Error fetching expenses:', error));
  }, []);

  // Prepare data for the BarChart
  const data = expenses.map(expense => ({
    name: `Event ${expense.event_id}`,
    amount: expense.amount,
  }));

  // Calculate total and average expenses
  const totalExpenses = expenses.reduce((total, expense) => total + expense.amount, 0);
  const averageExpense = totalExpenses / (expenses.length || 1);

  // Generate a brief summary
  const summary = `
    The total expenses across all events amount to $${totalExpenses.toFixed(2)}. 
    The average expense per event is $${averageExpense.toFixed(2)}. 
    It is important to monitor events with higher expenses to avoid budget overruns. 
    Consider analyzing the trends in spending to optimize future event budgets.
  `;

  return (
    <div className="report-page">
      <motion.header
        className="report-header"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <h1>Event Budget Report</h1>
        <p>Analyze event expenses and identify cost-saving opportunities.</p>
      </motion.header>

      <section className="summary-section">
        <h2>Summary</h2>
        <motion.div
          className="summary-box"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1.5 }}
        >
          <p>{summary}</p>
        </motion.div>
      </section>

      <section className="chart-section">
        <h2>Expense Analysis</h2>
        <motion.div
          className="chart-container"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 1.5 }}
        >
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="amount" fill="#A0522D" animationDuration={1500} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </section>

      <section className="math-section">
        <h2>Mathematical Insights</h2>
        <motion.div
          className="math-box"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1.5 }}
        >
          <p><strong>Total Expenses:</strong> ${totalExpenses.toFixed(2)}</p>
          <p><strong>Average Expense Per Event:</strong> ${averageExpense.toFixed(2)}</p>
        </motion.div>
      </section>

      <section className="insights-section">
        <h2>Additional Insights</h2>
        <motion.ul
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 1.5 }}
        >
          <li><strong>High-Expense Events:</strong> Monitor these events to prevent budget overruns.</li>
          <li><strong>Spending Trends:</strong> Analyze spending trends across event types to optimize future budgets.</li>
          <li><strong>Cost-Saving Strategies:</strong> Identify low-expense events and replicate their cost-saving strategies.</li>
        </motion.ul>
      </section>

      <footer>
        <Link to="/home" className="button">Back to Home</Link>
      </footer>
    </div>
  );
};

export default Report;
