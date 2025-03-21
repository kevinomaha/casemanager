import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

// Mock axios
jest.mock('axios', () => ({
  get: jest.fn(() => Promise.resolve({ data: { tasks: [] } }))
}));

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
  Link: ({ children, to }) => <a href={to}>{children}</a>
}));

describe('Dashboard component', () => {
  test('renders dashboard with user info when user is provided', () => {
    const mockUser = {
      profile: {
        given_name: 'John',
        family_name: 'Doe',
        email: 'john.doe@example.com'
      }
    };
    
    render(<Dashboard user={mockUser} />);
    
    // Check for user info
    expect(screen.getByText(/Welcome, John/i)).toBeInTheDocument();
  });

  test('renders dashboard without user info when user is not provided', () => {
    render(<Dashboard user={null} />);
    
    // User info should not be present
    expect(screen.queryByText(/Welcome, /i)).not.toBeInTheDocument();
  });
});
