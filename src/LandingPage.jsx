import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <div className="landing-content-wrapper">
        <header className="landing-header">
          <h1 className="landing-title">Welcome to the Event Planner</h1>
        </header>
        
        <section className="landing-content">
          <button className="landing-button" onClick={() => navigate('/login')}>Login</button>
          <button className="landing-button" onClick={() => navigate('/signup')}>Sign Up</button>
        </section>

        <section className="landing-features">
          <h2 className="section-title">Features</h2>
          <div className="feature-cards">
            <div className="feature-card">
              <h3>Easy Event Management</h3>
              <p>Organize events effortlessly with our intuitive platform.</p>
            </div>
            <div className="feature-card">
              <h3>Task Tracking</h3>
              <p>Stay on top of tasks with automated reminders and tracking.</p>
            </div>
            <div className="feature-card">
              <h3>Budget Planning</h3>
              <p>Keep your event on budget with our powerful tracking tools.</p>
            </div>
          </div>
        </section>

        <section className="landing-testimonials">
          <h2 className="section-title">What Our Users Say</h2>
          <div className="testimonial-cards">
            <div className="testimonial-card">
              <p>This platform made planning my wedding a breeze!</p>
              <p>- Jessica A.</p>
            </div>
            <div className="testimonial-card">
              <p>Our corporate events have never been more organized.</p>
              <p>- John D.</p>
            </div>
            <div className="testimonial-card">
              <p>I can not imagine managing events without it!</p>
              <p>- Sarah K.</p>
            </div>
          </div>
        </section>

        <footer className="landing-footer">
          <p>&copy; 2024 Event Planner. All rights reserved.</p>
        </footer>
      </div>
    </div>
  );
};

export default LandingPage;
