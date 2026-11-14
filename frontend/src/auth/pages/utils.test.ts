import { describe, it, expect, vi, beforeEach } from 'vitest';
import { navigateToHomeIfAuthenticated } from './utils';
import { isAuthenticated } from '../services/LoginService';

vi.mock('../services/LoginService', () => ({
  isAuthenticated: vi.fn(),
}));

describe('navigateToHomeIfAuthenticated', () => {
  const mockNavigate = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('navigates home when the session is authenticated', async () => {
    vi.mocked(isAuthenticated).mockResolvedValue(true);

    await navigateToHomeIfAuthenticated(mockNavigate);

    expect(mockNavigate).toHaveBeenCalledWith('/');
  });

  it('does not navigate when the session is unauthenticated', async () => {
    vi.mocked(isAuthenticated).mockResolvedValue(false);

    await navigateToHomeIfAuthenticated(mockNavigate);

    expect(mockNavigate).not.toHaveBeenCalled();
  });
});
