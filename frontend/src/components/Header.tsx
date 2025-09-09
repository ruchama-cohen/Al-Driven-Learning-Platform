import React from 'react';
import './Header.css';

interface HeaderProps {
  currentView: 'login' | 'register' | 'learn' | 'admin';
  setCurrentView: (view: 'login' | 'register' | 'learn' | 'admin') => void;
  currentUser: string | null;
  setCurrentUser: (userId: string | null) => void;
}

const Header: React.FC<HeaderProps> = ({ currentView, setCurrentView, currentUser, setCurrentUser }) => {
  const handleLogout = () => {
    setCurrentUser(null);
    setCurrentView('login');
  };

  return (
    <header className="header">
      <div className="header-content">
        <h1 className="logo">AI Learning Platform</h1>
        <nav className="nav">
          {!currentUser && (
            <>
              <button 
                className={`nav-btn ${currentView === 'login' ? 'active' : ''}`}
                onClick={() => setCurrentView('login')}
              >
                Login
              </button>
              <button 
                className={`nav-btn ${currentView === 'register' ? 'active' : ''}`}
                onClick={() => setCurrentView('register')}
              >
                Register
              </button>
            </>
          )}
          {currentUser && (
            <button 
              className={`nav-btn ${currentView === 'learn' ? 'active' : ''}`}
              onClick={() => setCurrentView('learn')}
            >
              Learn
            </button>
          )}
          <button 
            className={`nav-btn ${currentView === 'admin' ? 'active' : ''}`}
            onClick={() => setCurrentView('admin')}
          >
            Admin
          </button>
          {currentUser && (
            <button className="nav-btn logout-btn" onClick={handleLogout}>
              Logout
            </button>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;