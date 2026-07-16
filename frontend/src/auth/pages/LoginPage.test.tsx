import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { HTMLInputTypeAttribute } from 'react';
import LoginPage from './LoginPage';
import { getAccessTokenFromApi } from '../services/LoginService';
import { navigateToHomeIfToken } from './utils';
import { useAlertContext } from '../../core/store/AlertContext';

const mockNavigate = vi.fn();
const mockSetAlert = vi.fn();

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

vi.mock('../services/LoginService', () => ({
  getAccessTokenFromApi: vi.fn(),
}));

vi.mock('./utils', () => ({
  navigateToHomeIfToken: vi.fn(),
}));

vi.mock('../../core/store/AlertContext', () => ({
  useAlertContext: vi.fn(),
}));

const getInputByName = (name: string, type: HTMLInputTypeAttribute = 'text') => {
  const input = document.querySelector(`input[name="${name}"][type="${type}"]`);
  if (!(input instanceof HTMLInputElement)) {
    throw new Error(`Input not found: ${name}`);
  }
  return input;
};

describe('LoginPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAlertContext).mockReturnValue({ alert: null, setAlert: mockSetAlert });
  });

  it('renders login form fields and buttons', () => {
    render(<LoginPage />);

    expect(screen.getByText('English AI Tutor')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Log in' })).toBeInTheDocument();
    expect(getInputByName('username')).toBeInTheDocument();
    expect(getInputByName('password', 'password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Log in' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Register' })).toBeInTheDocument();
  });

  it('checks token on mount', () => {
    render(<LoginPage />);

    expect(navigateToHomeIfToken).toHaveBeenCalledWith(mockNavigate);
  });

  it('submits login and navigates home on success', async () => {
    const user = userEvent.setup();
    vi.mocked(getAccessTokenFromApi).mockResolvedValue('token');

    render(<LoginPage />);

    await user.type(getInputByName('username'), 'test@example.com');
    await user.type(getInputByName('password', 'password'), 'password123');
    await user.click(screen.getByRole('button', { name: 'Log in' }));

    await waitFor(() => {
      expect(getAccessTokenFromApi).toHaveBeenCalledWith({
        username: 'test@example.com',
        password: 'password123',
      });
      expect(mockSetAlert).toHaveBeenCalledWith(null);
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });

  it('shows error alert when login fails', async () => {
    const user = userEvent.setup();
    vi.mocked(getAccessTokenFromApi).mockResolvedValue(null);

    render(<LoginPage />);

    await user.type(getInputByName('username'), 'test@example.com');
    await user.type(getInputByName('password', 'password'), 'wrong-password');
    await user.click(screen.getByRole('button', { name: 'Log in' }));

    await waitFor(() => {
      expect(mockSetAlert).toHaveBeenCalledWith({
        type: 'error',
        message: 'Invalid email or password.',
      });
    });
  });

  it('navigates to register page when register button is clicked', async () => {
    const user = userEvent.setup();
    render(<LoginPage />);

    await user.click(screen.getByRole('button', { name: 'Register' }));

    expect(mockNavigate).toHaveBeenCalledWith('/register');
  });

  it('renders current alert message', () => {
    vi.mocked(useAlertContext).mockReturnValue({
      alert: { type: 'error', message: 'Invalid email or password.' },
      setAlert: mockSetAlert,
    });

    render(<LoginPage />);

    expect(screen.getByText('Invalid email or password.')).toBeInTheDocument();
  });
});
