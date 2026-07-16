import { describe, it, expect, vi, beforeEach } from 'vitest';
import apiClient from '../../core/apiClient';
import { getErrorMessage, registerUser, type RegisterFormData } from './RegisterService';
import type { ApiErrorResponse } from './RegisterService';

vi.mock('../../core/apiClient', () => ({
  default: {
    post: vi.fn(),
  },
}));

describe('RegisterService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('calls register endpoint with form data', async () => {
    const formData: RegisterFormData = {
      email: 'test@example.com',
      password_1: 'password123',
      password_2: 'password123',
    };

    await registerUser(formData);

    expect(apiClient.post).toHaveBeenCalledWith('/auth/register', formData);
  });

  it('returns generic message for existing user API detail', () => {
    const error = {
      response: {
        data: {
          detail: 'User already exists',
        },
      },
    } as ApiErrorResponse;

    const message = getErrorMessage(error);

    expect(message).toBe('Registration failed. Please try again.');
  });

  it('returns API detail message when present and different', () => {
    const error = {
      response: {
        data: {
          detail: 'Invalid payload',
        },
      },
    } as ApiErrorResponse;

    const message = getErrorMessage(error);

    expect(message).toBe('Invalid payload');
  });

  it('returns generic message when detail is missing', () => {
    const error = {
      response: {
        data: {},
      },
    } as ApiErrorResponse;

    const message = getErrorMessage(error);

    expect(message).toBe('Registration failed. Please try again.');
  });
});
