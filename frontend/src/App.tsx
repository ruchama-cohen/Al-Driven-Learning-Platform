import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import UserRegistration from './components/UserRegistration';
import SimpleLogin from './components/SimpleLogin';
import LearningDashboard from './components/LearningDashboard';
import AdminDashboard from './components/AdminDashboard';

function App() {
  const [currentView, setCurrentView] = useState<'login' | 'register' | 'learn' | 'admin'>('login');
  const [currentUser, setCurrentUser] = useState<string | null>(null);

  console.log('App state:', { currentView, currentUser });

  return (
    <div className="App">
      <Header 
        currentView={currentView} 
        setCurrentView={setCurrentView}
        currentUser={currentUser}
        setCurrentUser={setCurrentUser}
      />
      <main className="main-content">
        {currentView === 'login' && (
          <SimpleLogin 
            setCurrentUser={setCurrentUser} 
            setCurrentView={setCurrentView}
            switchToRegister={() => setCurrentView('register')}
          />
        )}
        {currentView === 'register' && (
          <UserRegistration 
            setCurrentUser={setCurrentUser} 
            setCurrentView={setCurrentView}
            switchToLogin={() => setCurrentView('login')}
          />
        )}
        {currentView === 'learn' && currentUser && (
          <LearningDashboard userId={currentUser} />
        )}
        {currentView === 'admin' && <AdminDashboard />}
      </main>
    </div>
  );
}

export default App;
