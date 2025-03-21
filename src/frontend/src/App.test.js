import { render, screen } from '@testing-library/react';
import { AuthProvider } from 'react-oidc-context';
import App from './App';

// Mock react-oidc-context library
jest.mock('react-oidc-context', () => {
  return {
    AuthProvider: ({ children }) => children,
    useAuth: () => {
      return {
        isLoading: false,
        isAuthenticated: false,
        signinRedirect: jest.fn(),
        error: null,
        activeNavigator: null
      };
    }
  };
});

// Mock react-router-dom
jest.mock('react-router-dom', () => {
  return {
    BrowserRouter: ({ children }) => children,
    Routes: ({ children }) => children,
    Route: ({ children }) => children,
    Link: ({ children }) => children,
    Navigate: () => <div>Navigate</div>,
  };
});

// Basic smoke test
test('renders without crashing', () => {
  render(<App />);
});
