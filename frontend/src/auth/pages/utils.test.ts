import { describe, it, expect, vi, beforeEach } from 'vitest';
import { waitFor } from '@testing-library/react';
import { navigateToHomeIfToken } from './utils';
import { getAccessTokenFromLocalStorage } from '../services/LoginService';

vi.mock('../services/LoginService', () => ({
  getAccessTokenFromLocalStorage: vi.fn(),
}));

describe('navigateToHomeIfToken', () => {
  const mockNavigate = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('navigates to home when token exists', async () => {
    vi.mocked(getAccessTokenFromLocalStorage).mockResolvedValue('token');

    await navigateToHomeIfToken(mockNavigate);

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });

  it('does not navigate when token does not exist', async () => {
    vi.mocked(getAccessTokenFromLocalStorage).mockResolvedValue(null);

    await navigateToHomeIfToken(mockNavigate);

    await waitFor(() => {
      expect(mockNavigate).not.toHaveBeenCalled();
    });
  });
});
