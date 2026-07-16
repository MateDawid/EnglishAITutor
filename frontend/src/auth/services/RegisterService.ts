import { AxiosError } from 'axios';
import apiClient from '../../core/apiClient';

/**
 * Type definition for the registration form data.
 */
export type RegisterFormData = {
  email: string;
  password_1: string;
  password_2: string;
};

/**
 * Type definition for the API error response.
 */
export type ApiErrorResponse = AxiosError<{ detail?: string }>;

/**
 * Function to register a new user.
 * 
 * @param {RegisterFormData} formData - Form data containing email and passwords.
 * @return {undefined} - No return value.
 */
export const registerUser = async (formData: RegisterFormData): Promise<undefined> => {
    await apiClient.post('/auth/register', formData);
};

/**
 * 
 * @param {ApiErrorResponse} error - The error object from the API response.
 * @returns {string} - The error message to display.
 */
export const getErrorMessage = (error: ApiErrorResponse): string => {
    let apiError: string | undefined = error?.response?.data?.detail;
    if (apiError === 'User already exists') {
        apiError = undefined;
    }
    return apiError || 'Registration failed. Please try again.';
};