import type { NavigateFunction } from "react-router-dom";
import { isAuthenticated } from "../services/LoginService";

/**
 * Checks the current browser session and navigates home when it is authenticated.
 * 
 * @param {NavigateFunction} navigate - The navigation function from react-router-dom.
 */
export const navigateToHomeIfAuthenticated = async (navigate: NavigateFunction): Promise<void> => {
  if (await isAuthenticated()) {
    navigate('/');
  }
};
