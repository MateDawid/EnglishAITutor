import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import apiClient from '../../core/apiClient';
import {
  getAccessTokenFromApi,
  getAccessTokenFromLocalStorage,
  removeAccessTokenFromLocalStorage,
  type LoginFormData,
} from './LoginService';
import { ACCESS_TOKEN_KEY } from '../../core/contants';

vi.mock('../../core/apiClient', () => ({
  default: {
    post: vi.fn(),
  },
}));

describe('LoginService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.localStorage.clear();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('reads access token from local storage', async () => {
    window.localStorage.setItem(ACCESS_TOKEN_KEY, 'saved-token');

    const token = await getAccessTokenFromLocalStorage();

    expect(token).toBe('saved-token');
  });

  it('removes access token from local storage', () => {
    window.localStorage.setItem(ACCESS_TOKEN_KEY, 'saved-token');

    removeAccessTokenFromLocalStorage();

    expect(window.localStorage.getItem(ACCESS_TOKEN_KEY)).toBeNull();
  });

  it('returns token and persists it when API login succeeds', async () => {
    const formData: LoginFormData = { username: 'test@example.com', password: 'password123' };
    vi.mocked(apiClient.post).mockResolvedValue({ data: { access_token: 'api-token' } });

    const token = await getAccessTokenFromApi(formData);

    expect(apiClient.post).toHaveBeenCalledWith('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    expect(token).toBe('api-token');
    expect(window.localStorage.getItem(ACCESS_TOKEN_KEY)).toBe('api-token');
  });

  it('returns null and clears storage when API login fails', async () => {
    const formData: LoginFormData = { username: 'test@example.com', password: 'bad-password' };
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    window.localStorage.setItem(ACCESS_TOKEN_KEY, 'old-token');
    vi.mocked(apiClient.post).mockRejectedValue(new Error('Unauthorized'));

    const token = await getAccessTokenFromApi(formData);

    expect(token).toBeNull();
    expect(window.localStorage.getItem(ACCESS_TOKEN_KEY)).toBeNull();
    expect(consoleErrorSpy).toHaveBeenCalled();
  });
});
