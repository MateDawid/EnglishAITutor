import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BasePage } from './BasePage';
import { getAccessTokenFromLocalStorage } from '../../auth/services/LoginService';
import { useAlertContext } from '../store/AlertContext';

const mockNavigate = vi.fn();
const mockSetAlert = vi.fn();

vi.mock('react-router-dom', () => ({
  Outlet: () => <div data-testid="outlet" />,
  useNavigate: () => mockNavigate,
}));

vi.mock('../components/Navbar', () => ({
  Navbar: () => <div data-testid="navbar" />,
}));

vi.mock('../../auth/services/LoginService', () => ({
  getAccessTokenFromLocalStorage: vi.fn(),
}));

vi.mock('../store/AlertContext', () => ({
  useAlertContext: vi.fn(),
}));

describe('BasePage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAlertContext).mockReturnValue({ alert: null, setAlert: mockSetAlert });
  });

  it('renders navbar and outlet content', () => {
    vi.mocked(getAccessTokenFromLocalStorage).mockReturnValue('token');

    render(<BasePage />);

    expect(screen.getByTestId('navbar')).toBeInTheDocument();
    expect(screen.getByTestId('outlet')).toBeInTheDocument();
  });

  it('navigates to login when token does not exist', async () => {
    vi.mocked(getAccessTokenFromLocalStorage).mockReturnValue(null);

    render(<BasePage />);

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/login');
    });
  });

  it('does not navigate when token exists', async () => {
    vi.mocked(getAccessTokenFromLocalStorage).mockReturnValue('token');

    render(<BasePage />);

    await waitFor(() => {
      expect(mockNavigate).not.toHaveBeenCalled();
    });
  });

  it('shows snackbar alert message when alert exists', () => {
    vi.mocked(getAccessTokenFromLocalStorage).mockReturnValue('token');
    vi.mocked(useAlertContext).mockReturnValue({
      alert: { type: 'success', message: 'Done' },
      setAlert: mockSetAlert,
    });

    render(<BasePage />);

    expect(screen.getByText('Done')).toBeInTheDocument();
  });
});
