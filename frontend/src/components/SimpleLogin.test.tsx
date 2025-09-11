import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SimpleLogin from './SimpleLogin';

// Mock fetch
global.fetch = jest.fn();

describe('SimpleLogin Component', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  test('renders login form', () => {
    const mockProps = {
      setCurrentUser: jest.fn(),
      setCurrentView: jest.fn()
    };
    
    render(<SimpleLogin {...mockProps} />);
    
    expect(screen.getByPlaceholderText('שם מלא')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('מספר טלפון')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('תעודת זהות')).toBeInTheDocument();
    expect(screen.getByText('התחבר')).toBeInTheDocument();
  });

  test('submits form with correct data', async () => {
    const mockSetCurrentUser = jest.fn();
    const mockSetCurrentView = jest.fn();
    
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: '123', message: 'Login successful' })
    });

    render(
      <SimpleLogin 
        setCurrentUser={mockSetCurrentUser}
        setCurrentView={mockSetCurrentView}
      />
    );

    fireEvent.change(screen.getByPlaceholderText('שם מלא'), {
      target: { value: 'Test User' }
    });
    fireEvent.change(screen.getByPlaceholderText('מספר טלפון'), {
      target: { value: '1234567890' }
    });
    fireEvent.change(screen.getByPlaceholderText('תעודת זהות'), {
      target: { value: '123456789' }
    });

    fireEvent.click(screen.getByText('התחבר'));

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: 'Test User',
          phone: '1234567890',
          id_number: '123456789'
        })
      });
    });

    expect(mockSetCurrentUser).toHaveBeenCalledWith('123');
    expect(mockSetCurrentView).toHaveBeenCalledWith('learn');
  });

  test('shows error on failed login', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'User not found' })
    });

    render(
      <SimpleLogin 
        setCurrentUser={jest.fn()}
        setCurrentView={jest.fn()}
      />
    );

    fireEvent.click(screen.getByText('התחבר'));

    await waitFor(() => {
      expect(screen.getByText(/שגיאה/)).toBeInTheDocument();
    });
  });
});