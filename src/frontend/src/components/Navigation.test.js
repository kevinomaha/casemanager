import { render, screen } from '@testing-library/react';
import Navigation from './Navigation';

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
  Link: ({ children, to }) => <a href={to}>{children}</a>
}));

// Mock react-oidc-context
jest.mock('react-oidc-context', () => ({
  useAuth: () => ({
    isAuthenticated: true,
    signoutRedirect: jest.fn()
  })
}));

describe('Navigation component', () => {
  test('renders navigation links', () => {
    render(<Navigation />);
    
    // Check for Dashboard link
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    
    // Check for Tasks link
    expect(screen.getByText('Tasks')).toBeInTheDocument();
    
    // Check for Auth Debug link
    expect(screen.getByText('Auth Debug')).toBeInTheDocument();
  });
});
