import { describe, it, expect, vi, beforeEach } from 'vitest';
import apiClient from '../../core/apiClient';
import { isAuthenticated, loginUser, logoutUser, type LoginFormData } from './LoginService';

vi.mock('../../core/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('LoginService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.localStorage.clear();
  });

  it('submits credentials to the login endpoint without storing a token', async () => {
    const formData: LoginFormData = { username: 'test@example.com', password: 'password123' };
    vi.mocked(apiClient.post).mockResolvedValue({ data: { id: 'user-id' } });

    await loginUser(formData);

    expect(apiClient.post).toHaveBeenCalledWith('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    expect(window.localStorage.length).toBe(0);
  });

  it('reports an authenticated cookie session', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: { id: 'user-id' } });

    await expect(isAuthenticated()).resolves.toBe(true);
    expect(apiClient.get).toHaveBeenCalledWith('/auth/me');
  });

  it('reports an expired cookie session as unauthenticated', async () => {
    const unauthorizedError = Object.assign(new Error('Unauthorized'), {
      isAxiosError: true,
      response: { status: 401 },
    });
    vi.mocked(apiClient.get).mockRejectedValue(unauthorizedError);

    await expect(isAuthenticated()).resolves.toBe(false);
  });

  it('propagates unexpected session-check errors', async () => {
    const error = new Error('Network error');
    vi.mocked(apiClient.get).mockRejectedValue(error);

    await expect(isAuthenticated()).rejects.toBe(error);
  });

  it('logs out through the API', async () => {
    vi.mocked(apiClient.post).mockResolvedValue({ data: undefined });

    await logoutUser();

    expect(apiClient.post).toHaveBeenCalledWith('/auth/logout');
  });
});
