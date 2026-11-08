import axios from "axios";
import apiClient from "../../core/apiClient";

/**
 * Type definition for the login form data.
 */
export type LoginFormData = {
  username: string;
  password: string;
};


/**
 * Authenticate the user and establish a cookie-based session.
 *
 * @param {LoginFormData} formData - The login form data.
 * @returns {Promise<void>} Resolves when authentication succeeds.
 */
export const loginUser = async (formData: LoginFormData): Promise<void> => {
  await apiClient.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};

/**
 * Check whether the current browser session is authenticated.
 *
 * @returns {Promise<boolean>} Whether the current session is authenticated.
 */
export const isAuthenticated = async (): Promise<boolean> => {
  try {
    await apiClient.get("/auth/me");
    return true;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      return false;
    }

    throw error;
  }
};

/**
 * End the current browser session.
 *
 * @returns {Promise<void>} Resolves when the server clears the session cookie.
 */
export const logoutUser = async (): Promise<void> => {
  await apiClient.post("/auth/logout");
};