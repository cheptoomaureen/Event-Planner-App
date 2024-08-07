
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="homepage">
      <header className="header">
        <h1>Welcome to Event Planner</h1>
      </header>

      
      <section className="dashboard">
        <h2>Dashboard Overview</h2>
        <div className="dashboard-item">
          <h3>Upcoming Events</h3>
          <p>Organize your events by categories like personal, professional, and social.</p>
          <button className="button">View Events</button>
        </div>
        <div className="dashboard-item">
          <h3>Tasks and Deadlines</h3>
          <p>Assign tasks, set deadlines, and track progress easily.</p>
          <button className="button">View Tasks</button>
        </div>
        <div className="dashboard-item">
          <h3>Resource Management</h3>
          <p>Efficiently manage resources like venues and equipment.</p>
          <button className="button">Manage Resources</button>
        </div>
        <div className="dashboard-item">
          <h3>Budget Tracking</h3>
          <p>Monitor spending and stay within your event budget.</p>
          <button className="button">View Budgets</button>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
