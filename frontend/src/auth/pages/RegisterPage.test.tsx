import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { HTMLInputTypeAttribute } from 'react';
import RegisterPage from './RegisterPage';
import { getErrorMessage, registerUser } from '../services/RegisterService';
import { navigateToHomeIfToken } from './utils';
import { useAlertContext } from '../../core/store/AlertContext';
import type { ApiErrorResponse } from '../services/RegisterService';

const mockNavigate = vi.fn();
const mockSetAlert = vi.fn();

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

vi.mock('../services/RegisterService', () => ({
  registerUser: vi.fn(),
  getErrorMessage: vi.fn(),
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

describe('RegisterPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAlertContext).mockReturnValue({ alert: null, setAlert: mockSetAlert });
  });

  it('renders registration form fields and buttons', () => {
    render(<RegisterPage />);

    expect(screen.getByText('English AI Tutor')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: 'Register' })).toBeInTheDocument();
    expect(getInputByName('email')).toBeInTheDocument();
    expect(getInputByName('password_1', 'password')).toBeInTheDocument();
    expect(getInputByName('password_2', 'password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Register' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Log in' })).toBeInTheDocument();
  });

  it('checks token on mount', () => {
    render(<RegisterPage />);

    expect(navigateToHomeIfToken).toHaveBeenCalledWith(mockNavigate);
  });

  it('submits register form and sets success alert on success', async () => {
    const user = userEvent.setup();
    vi.mocked(registerUser).mockResolvedValue(undefined);

    render(<RegisterPage />);

    await user.type(getInputByName('email'), 'test@example.com');
    await user.type(getInputByName('password_1', 'password'), 'password123');
    await user.type(getInputByName('password_2', 'password'), 'password123');
    await user.click(screen.getByRole('button', { name: 'Register' }));

    await waitFor(() => {
      expect(registerUser).toHaveBeenCalledWith({
        email: 'test@example.com',
        password_1: 'password123',
        password_2: 'password123',
      });
      expect(mockSetAlert).toHaveBeenCalledWith({
        type: 'success',
        message: 'Registration successful.',
      });
    });
  });

  it('sets error alert on failed registration', async () => {
    const user = userEvent.setup();
    const error = { response: { data: { detail: 'bad' } } } as ApiErrorResponse;
    vi.mocked(registerUser).mockRejectedValue(error);
    vi.mocked(getErrorMessage).mockReturnValue('Registration failed');

    render(<RegisterPage />);

    await user.type(getInputByName('email'), 'test@example.com');
    await user.type(getInputByName('password_1', 'password'), 'password123');
    await user.type(getInputByName('password_2', 'password'), 'password123');
    await user.click(screen.getByRole('button', { name: 'Register' }));

    await waitFor(() => {
      expect(getErrorMessage).toHaveBeenCalledWith(error);
      expect(mockSetAlert).toHaveBeenCalledWith({
        type: 'error',
        message: 'Registration failed',
      });
    });
  });

  it('navigates to login page when log in button is clicked', async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    await user.click(screen.getByRole('button', { name: 'Log in' }));

    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });

  it('renders current alert message', () => {
    vi.mocked(useAlertContext).mockReturnValue({
      alert: { type: 'error', message: 'Registration failed' },
      setAlert: mockSetAlert,
    });

    render(<RegisterPage />);

    expect(screen.getByText('Registration failed')).toBeInTheDocument();
  });
});
