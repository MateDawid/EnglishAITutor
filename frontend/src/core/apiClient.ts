import axios, { type AxiosResponse } from "axios";
import { ACCESS_TOKEN_KEY } from "./contants";

function isAuthRequest(url: string): boolean {
  return url.includes("/auth/login") || url.includes("/auth/register");
}

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Axios response interceptor to handle 401 Unauthorized errors.
 * If the request is not an authentication request and the response status is 401,
 * the access token is removed from local storage and the user is redirected to the login page.
 * 
 * @param {AxiosResponse} response - The Axios response object.
 * @return {AxiosResponse} - The Axios response object or a rejected promise with the error.
 */
client.interceptors.response.use(
  (response): AxiosResponse => {
    return response;
  },
  (error): Promise<never> => {
    if (!isAuthRequest(error.response.request.responseURL) && error.response?.status === 401) {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);


export default client;