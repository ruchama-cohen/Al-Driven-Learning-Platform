import React, { useState } from 'react';

interface SimpleLoginProps {
  setCurrentUser: (userId: string) => void;
  setCurrentView: (view: 'register' | 'learn' | 'admin') => void;
  switchToRegister: () => void;
}

const SimpleLogin: React.FC<SimpleLoginProps> = ({ setCurrentUser, setCurrentView, switchToRegister }) => {
  const [formData, setFormData] = useState({ name: '', phone: '', id_number: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const result = await response.json();
        if (result.id) {
          setCurrentUser(result.id);
          setCurrentView('learn');
        }
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Login failed');
      }
    } catch (error) {
      console.error('Network error:', error);
      alert('Network error: Cannot connect to server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Login to AI Learning Platform</h2>
      <p>Enter your exact name and phone as registered</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Name:</label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            required
          />
        </div>
        <div className="form-group">
          <label>Phone:</label>
          <input
            type="text"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            required
          />
        </div>
        <div className="form-group">
          <label>ID Number:</label>
          <input
            type="text"
            value={formData.id_number}
            onChange={(e) => setFormData({...formData, id_number: e.target.value})}
            required
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
          onClick={switchToRegister}
          style={{ background: 'none', border: 'none', color: '#007bff', textDecoration: 'underline', cursor: 'pointer' }}
        >
          Register here
        </button>
      </p>
    </div>
  );
};

export default SimpleLogin;