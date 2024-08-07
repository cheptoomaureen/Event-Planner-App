import  { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginSignupPage.css';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (event) => {
    event.preventDefault();

    const url = 'http://localhost:5555/auth/login';
    const data = { email, password };

    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Invalid login credentials');
        }
      })
      .then((data) => {
        localStorage.setItem('token', data.token);
        alert('WELCOME to Event Planner...');
        navigate('/home');
      })
      .catch((error) => {
        console.error('Error:', error);
        alert('Invalid login credentials. Please try again.');
      });
  };

  return (
    <div className="container">
      <header>
        <h1>Login</h1>
      </header>
      <section>
        <form className="login" onSubmit={handleLogin}>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            required
          />
          <br />
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
          <button type="submit">Login</button>
        </form>
      </section>
    </div>
  );
};

export default LoginPage;
