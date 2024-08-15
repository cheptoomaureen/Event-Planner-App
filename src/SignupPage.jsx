import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginSignupPage.css';

const SignupPage = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignup = (event) => {
    event.preventDefault();

    const signupUrl = 'http://localhost:5555/auth/register';
    const signupData = { username, email, password };

    fetch(signupUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(signupData),
    })
      .then((response) => {
        if (response.ok) {
          alert('Registration successful. Please log in to continue.');
          navigate('/login');
        } else {
          throw new Error('Error during signup: ' + response.status);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
      });
  };

  const goToLoginPage = () => {
    navigate('/login');
  };

  return (
    <div className="container">
      <header>
        <h1>Sign Up</h1>
      </header>
      <section>
        <form onSubmit={handleSignup}>
          <label htmlFor="username">Name:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Name"
            required
          />
          <br />
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
          <button type="submit">Sign Up</button>
        </form>
      </section>
      <footer>
        <button onClick={goToLoginPage}>Go to Login Page</button>
      </footer>
    </div>
  );
};

export default SignupPage;
