import apiClient from "../../core/apiClient";
import { ACCESS_TOKEN_KEY } from "../../core/contants";


/**
 * Function to get User access token.
 * @return {string | null} - User access token or null.
 */
export const getAccessTokenFromLocalStorage = async (): Promise<string | null> => {
    return window.localStorage.getItem(ACCESS_TOKEN_KEY);
};

/**
 * Function to get User access token from API.
 * 
 * @param {string} email - User email.
 * @param {string} password - User password.
 * @return {string | null} - User access token or null.
 */
export const getAccessTokenFromApi = async (email: string, password: string): Promise<string | null> => {
    try {
        const response = await apiClient.post(
            '/auth/login',
            {
                username: email,
                password: password,
            },
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