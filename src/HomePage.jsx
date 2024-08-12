import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="homepage">
      <header className="header">
        <h1>Welcome to Our Event Management Platform</h1>
        <p>Effortlessly manage events, tasks, resources, and budgets with our all-in-one solution.</p>
      </header>

      <section className="dashboard">
        <h2>Dashboard Overview</h2>
        <div className="dashboard-grid">
          <div className="dashboard-item">
            <i className="fas fa-calendar-alt"></i>
            <h3>Upcoming Events</h3>
            <p>Organize your events by categories like personal, professional, and social.</p>
            <Link to="/events" className="button">View Events</Link>
          </div>
          <div className="dashboard-item">
            <i className="fas fa-tasks"></i>
            <h3>Tasks and Deadlines</h3>
            <p>Assign tasks, set deadlines, and track progress easily.</p>
            <Link to="/tasks" className="button">View Tasks</Link>
          </div>
          <div className="dashboard-item">
            <i className="fas fa-cogs"></i>
            <h3>Resource Management</h3>
            <p>Efficiently manage resources like venues and equipment.</p>
            <Link to="/resources" className="button">Manage Resources</Link>
          </div>
          <div className="dashboard-item">
            <i className="fas fa-dollar-sign"></i>
            <h3>Budget Tracking</h3>
            <p>Monitor spending and stay within your event budget.</p>
            <Link to="/budget" className="button">View Budgets</Link>
          </div>
          <div className="dashboard-item">
            <i className="fas fa-users"></i>
            <h3>Team Collaboration</h3>
            <p>Work together with your team in real-time with our collaboration tools.</p>
            <Link to="/collaboration" className="button">Collaborate</Link> {/* Ensure this Link is correct */}
          </div>
          <div className="dashboard-item">
            <i className="fas fa-chart-line"></i>
            <h3>Analytics and Reports</h3>
            <p>Get detailed insights into your events, tasks, and budgets.</p>
            <Link to="/report" className="button">View Reports</Link>
          </div>
        </div>
      </section>

      <section className="services">
        <h2>Why Choose Us?</h2>
        <div className="services-grid">
          <div className="service-item">
            <i className="fas fa-lock"></i>
            <h3>Secure and Reliable</h3>
            <p>Your data is safe with us, protected by the latest security measures.</p>
          </div>
          <div className="service-item">
            <i className="fas fa-sync-alt"></i>
            <h3>Real-Time Updates</h3>
            <p>Instant notifications and real-time updates keep you on top of your tasks.</p>
          </div>
          <div className="service-item">
            <i className="fas fa-mobile-alt"></i>
            <h3>Mobile Friendly</h3>
            <p>Access and manage your events on the go with our mobile-optimized platform.</p>
          </div>
          <div className="service-item">
            <i className="fas fa-headset"></i>
            <h3>24/7 Support</h3>
            <p>Our support team is available around the clock to assist you with any issues.</p>
          </div>
        </div>
      </section>

      <footer>
        <Link to="/" className="button">Logout</Link>
      </footer>
    </div>
  );
};

export default HomePage;
