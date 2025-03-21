import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the dashboard component that imports axios
jest.mock('./components/Dashboard', () => {
  return function MockDashboard() {
    return <div data-testid="dashboard-mock">Dashboard Mock</div>;
  };
});

// Mock TasksList component
jest.mock('./components/TasksList', () => {
  return function MockTasksList() {
    return <div data-testid="tasks-list-mock">Tasks List Mock</div>;
  };
});

// Mock TaskDetail component
jest.mock('./components/TaskDetail', () => {
  return function MockTaskDetail() {
    return <div data-testid="task-detail-mock">Task Detail Mock</div>;
  };
});

// Mock react-oidc-context library
jest.mock('react-oidc-context', () => {
  return {
    AuthProvider: ({ children }) => children,
    useAuth: () => {
      return {
        isLoading: false,
        isAuthenticated: false,
        signinRedirect: jest.fn(),
        signoutRedirect: jest.fn(),
        error: null,
        activeNavigator: null,
        user: null
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
    useNavigate: () => jest.fn(),
    Outlet: () => <div>Outlet</div>
  };
});

// Basic smoke test
test('renders without crashing', () => {
  render(<App />);
});
