import { describe, it, expect, vi, beforeEach } from 'vitest';

type InterceptorError = {
  response?: {
    status?: number;
    data?: unknown;
  };
  config?: {
    url?: string;
    csrfRetry?: boolean;
  };
};

type RequestConfig = {
  method?: string;
  headers: Record<string, string>;
  withCredentials?: boolean;
};

const { createMock, getMock, requestMock, requestUseMock, responseUseMock } = vi.hoisted(() => ({
  createMock: vi.fn(),
  getMock: vi.fn(),
  requestMock: vi.fn(),
  requestUseMock: vi.fn(),
  responseUseMock: vi.fn(),
}));

vi.mock('axios', () => ({
  default: {
    create: createMock.mockImplementation(() => ({
      get: getMock,
      request: requestMock,
      interceptors: {
        request: {
          use: requestUseMock,
        },
        response: {
          use: responseUseMock,
        },
      },
    })),
  },
}));

import client from './apiClient';

describe('apiClient interceptors', () => {
  beforeEach(() => {
    window.history.pushState({}, '', '/');
  });

  it('creates an axios instance with cookie credentials enabled', () => {
    expect(client).toBeDefined();
    expect(createMock).toHaveBeenCalledWith({
      baseURL: import.meta.env.VITE_API_URL,
      timeout: 10000,
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  });

  it('adds a cached in-memory CSRF token to unsafe requests', async () => {
    getMock.mockResolvedValue({ data: { csrf_token: 'signed-csrf-token' } });
    const requestHandler = requestUseMock.mock.calls[0][0] as (
      config: RequestConfig
    ) => Promise<RequestConfig>;

    const result = await requestHandler({ method: 'post', headers: {} });

    expect(getMock).toHaveBeenCalledWith('/auth/csrf');
    expect(result.withCredentials).toBe(true);
    expect(result.headers['X-CSRF-Token']).toBe('signed-csrf-token');
  });

  it('returns a successful response unchanged', () => {
    const successHandler = responseUseMock.mock.calls[0][0] as (response: unknown) => unknown;
    const response = { data: { ok: true } };

    expect(successHandler(response)).toBe(response);
  });

  it('redirects to login after a 401 from a protected endpoint', async () => {
    const errorHandler = responseUseMock.mock.calls[0][1] as (
      error: InterceptorError
    ) => Promise<unknown>;
    const error = {
      config: { url: '/flashcards/' },
      response: { status: 401 },
    };

    await expect(errorHandler(error)).rejects.toBe(error);
    expect(window.location.href).toContain('/login');
  });

  it('does not redirect after a 401 from an authentication endpoint', async () => {
    const errorHandler = responseUseMock.mock.calls[0][1] as (
      error: InterceptorError
    ) => Promise<unknown>;
    const originalHref = window.location.href;
    const error = {
      config: { url: '/auth/login' },
      response: { status: 401 },
    };

    await expect(errorHandler(error)).rejects.toBe(error);
    expect(window.location.href).toBe(originalHref);
  });

  it('refreshes the CSRF token and retries a request once after CSRF expiry', async () => {
    const errorHandler = responseUseMock.mock.calls[0][1] as (
      error: InterceptorError
    ) => Promise<unknown>;
    const config: InterceptorError['config'] = { url: '/auth/register' };
    const error = {
      config,
      response: {
        status: 403,
        data: { detail: 'Missing or invalid CSRF token' },
      },
    };
    requestMock.mockResolvedValue({ data: { ok: true } });

    await errorHandler(error);

    expect(config.csrfRetry).toBe(true);
    expect(requestMock).toHaveBeenCalledWith(config);
  });
});
