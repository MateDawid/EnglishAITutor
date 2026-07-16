import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ACCESS_TOKEN_KEY } from './contants';

type InterceptorError = {
  response?: {
    status?: number;
    request: {
      responseURL: string;
    };
  };
};

const { createMock, responseUseMock } = vi.hoisted(() => ({
  createMock: vi.fn(),
  responseUseMock: vi.fn(),
}));

vi.mock('axios', () => ({
  default: {
    create: createMock.mockImplementation(() => ({
      interceptors: {
        response: {
          use: responseUseMock,
        },
      },
    })),
  },
}));

import client from './apiClient';

describe('apiClient', () => {
  beforeEach(() => {
    window.localStorage.clear();
    window.history.pushState({}, '', '/');
  });

  it('creates axios instance with expected defaults', () => {
    expect(client).toBeDefined();
    expect(createMock).toHaveBeenCalledWith({
      baseURL: import.meta.env.VITE_API_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  });

  it('returns response unchanged in success interceptor', () => {
    const successHandler = responseUseMock.mock.calls[0][0] as (response: unknown) => unknown;
    const response = { data: { ok: true } };

    const result = successHandler(response);

    expect(result).toBe(response);
  });

  it('removes token and redirects to login on 401 from non-auth endpoint', async () => {
    const errorHandler = responseUseMock.mock.calls[0][1] as (error: InterceptorError) => Promise<never>;
    window.localStorage.setItem(ACCESS_TOKEN_KEY, 'token');

    const error = {
      response: {
        status: 401,
        request: {
          responseURL: 'https://api.example.com/protected/resource',
        },
      },
    };

    await expect(errorHandler(error)).rejects.toBe(error);

    expect(window.localStorage.getItem(ACCESS_TOKEN_KEY)).toBeNull();
    expect(window.location.href).toContain('/login');
  });

  it('does not redirect on 401 from auth endpoints', async () => {
    const errorHandler = responseUseMock.mock.calls[0][1] as (error: InterceptorError) => Promise<never>;
    window.localStorage.setItem(ACCESS_TOKEN_KEY, 'token');
    const originalHref = window.location.href;

    const error = {
      response: {
        status: 401,
        request: {
          responseURL: 'https://api.example.com/auth/login',
        },
      },
    };

    await expect(errorHandler(error)).rejects.toBe(error);

    expect(window.localStorage.getItem(ACCESS_TOKEN_KEY)).toBe('token');
    expect(window.location.href).toBe(originalHref);
  });
});
