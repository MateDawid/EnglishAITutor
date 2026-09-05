import { describe, it, expect, vi, beforeEach } from 'vitest';
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

  it('navigates to home when token exists', () => {
    vi.mocked(getAccessTokenFromLocalStorage).mockReturnValue('token');

    navigateToHomeIfToken(mockNavigate);

    expect(mockNavigate).toHaveBeenCalledWith('/');
  });

  it('does not navigate when token does not exist', () => {
    vi.mocked(getAccessTokenFromLocalStorage).mockReturnValue(null);

    navigateToHomeIfToken(mockNavigate);

    expect(mockNavigate).not.toHaveBeenCalled();
  });
});
