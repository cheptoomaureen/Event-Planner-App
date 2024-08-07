
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <header>
        <h1>Welcome to the Event Planner</h1>
      </header>
      <section>
        <button className="landing-button" onClick={() => navigate('/login')}>Login</button>
        <button className="landing-button" onClick={() => navigate('/signup')}>Sign Up</button>
      </section>
      <footer className="footer">
        <p>&copy; 2024 Event Planner. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default LandingPage;
