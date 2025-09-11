import React, { useState } from 'react';

interface UserLoginProps {
  setCurrentUser: (userId: string) => void;
  setCurrentView: (view: 'login' | 'register' | 'learn' | 'admin') => void;
}

const UserLogin: React.FC<UserLoginProps> = ({ setCurrentUser, setCurrentView }) => {
  const [formData, setFormData] = useState({ name: '', phone: '', id_number: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    console.log('Login attempt:', formData);

    try {
      const response = await fetch('http://localhost:8000/api/users/login-jwt', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      const result = await response.json();
      console.log('Response data:', result);

      if (response.ok && result.access_token) {
        localStorage.setItem('access_token', result.access_token);
        localStorage.setItem('user_id', result.user_id);
        console.log('Login successful, user ID:', result.user_id);
        setCurrentUser(result.user_id);
        setCurrentView('learn');
      } else {
        const errorMessage = result.detail || result.error || 'Login failed';
        console.error('Login failed:', errorMessage);
        setError(errorMessage);
      }
    } catch (error) {
      console.error('Network error:', error);
      setError('Network error: Cannot connect to server. Please check if the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Login to AI Learning Platform</h2>
      
      {error && (
        <div style={{ 
          color: 'red', 
          padding: '10px', 
          marginBottom: '10px',
          border: '1px solid red',
          borderRadius: '4px',
          backgroundColor: '#ffe6e6'
        }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name:</label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            required
            placeholder="Enter your name"
          />
        </div>
        
        <div className="form-group">
          <label>Phone:</label>
          <input
            type="text"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            required
            placeholder="Enter your phone number"
          />
        </div>
        
        <div className="form-group">
          <label>ID Number:</label>
          <input
            type="text"
            value={formData.id_number}
            onChange={(e) => setFormData({...formData, id_number: e.target.value})}
            required
            placeholder="Enter your ID number"
          />
        </div>
        
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      
      <p style={{ marginTop: '20px', textAlign: 'center' }}>
        Don't have an account?{' '}
        <button
          type="button"
          className="btn btn-link"
          onClick={() => setCurrentView('register')}
          style={{ 
            background: 'none', 
            border: 'none', 
            color: '#007bff', 
            textDecoration: 'underline', 
            cursor: 'pointer' 
          }}
        >
          Register here
        </button>
      </p>
    </div>
  );
};

export default UserLogin;