import type { NavigateFunction } from "react-router-dom";
import { getAccessTokenFromLocalStorage } from "../services/LoginService";

/**
 * Checks if an access token exists in local storage and navigates to the home page if it does.
 * 
 * @param {NavigateFunction} navigate - The navigation function from react-router-dom.
 */
export const navigateToHomeIfToken= async (navigate: NavigateFunction) => {
  getAccessTokenFromLocalStorage().then((token) => {
    if (token) {
      navigate('/');
    }
  });
};
