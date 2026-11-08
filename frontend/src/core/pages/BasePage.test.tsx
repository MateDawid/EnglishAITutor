import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BasePage } from './BasePage';
import { isAuthenticated } from '../../auth/services/LoginService';
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
  isAuthenticated: vi.fn(),
}));

vi.mock('../store/AlertContext', () => ({
  useAlertContext: vi.fn(),
}));

describe('BasePage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(useAlertContext).mockReturnValue({ alert: null, setAlert: mockSetAlert });
    vi.mocked(isAuthenticated).mockResolvedValue(true);
  });

  it('renders navbar and outlet content', () => {
    render(<BasePage />);

    expect(screen.getByTestId('navbar')).toBeInTheDocument();
    expect(screen.getByTestId('outlet')).toBeInTheDocument();
  });

  it('navigates to login when the session is not authenticated', async () => {
    vi.mocked(isAuthenticated).mockResolvedValue(false);

    render(<BasePage />);

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/login', { replace: true });
    });
  });

  it('does not navigate when the session is authenticated', async () => {
    vi.mocked(isAuthenticated).mockResolvedValue(true);

    render(<BasePage />);

    await waitFor(() => {
      expect(mockNavigate).not.toHaveBeenCalled();
    });
  });

  it('shows snackbar alert message when alert exists', () => {
    vi.mocked(useAlertContext).mockReturnValue({
      alert: { type: 'success', message: 'Done' },
      setAlert: mockSetAlert,
    });

    render(<BasePage />);

    expect(screen.getByText('Done')).toBeInTheDocument();
  });
});
