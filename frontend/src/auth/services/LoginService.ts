import apiClient from "../../core/apiClient";
import { ACCESS_TOKEN_KEY } from "../../core/contants";

/**
 * Type definition for the login form data.
 */
export type LoginFormData = {
  username: string;
  password: string;
};


/**
 * Function to get User access token.
 * @return {string | null} - User access token or null.
 */
export const getAccessTokenFromLocalStorage = (): string | null => {
    return window.localStorage.getItem(ACCESS_TOKEN_KEY);
};

/**
 * Function to get User access token from API.
 * 
 * @param {string} email - User email.
 * @param {string} password - User password.
 * @return {string | null} - User access token or null.
 */
export const getAccessTokenFromApi = async (formData: LoginFormData): Promise<string | null> => {
    try {
        const response = await apiClient.post(
            '/auth/login',
            formData,
            {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            }
        );
        const token = response.data.access_token
        window.localStorage.setItem(ACCESS_TOKEN_KEY, token);
        return token;
    } catch (error) {
        console.error(error);
        window.localStorage.removeItem(ACCESS_TOKEN_KEY);
        return null;
    }
};

export const removeAccessTokenFromLocalStorage = (): void => {
    window.localStorage.removeItem(ACCESS_TOKEN_KEY);
};