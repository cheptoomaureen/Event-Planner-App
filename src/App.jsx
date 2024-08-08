
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './LandingPage';
import LoginPage from './LoginPage';
import SignupPage from './SignupPage';
import HomePage from './HomePage';
import './App.css';
import Tasks from './Tasks';
import Resources from './Resources';
import Collaboration from './Collaboration';
import Budget from './Budget';
import Events from './Events';
import Report from './Report'
const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/resources" element={<Resources />} />
        <Route path="/collaboration" element={<Collaboration />} />
        <Route path="/budget" element={<Budget />} />
        <Route path="/events" element={<Events />} />
        <Route path="/report" element={<Report/>} />
       
      </Routes>
    </Router>
  );
};

export default App;
