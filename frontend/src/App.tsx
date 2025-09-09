import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import UserRegistration from './components/UserRegistration';
import UserLogin from './components/UserLogin';
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
          <UserLogin setCurrentUser={setCurrentUser} setCurrentView={setCurrentView} />
        )}
        {currentView === 'register' && (
          <UserRegistration setCurrentUser={setCurrentUser} setCurrentView={setCurrentView} />
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
