import axios, { type AxiosError, type AxiosResponse } from "axios";

declare module "axios" {
  interface InternalAxiosRequestConfig {
    csrfRetry?: boolean;
  }
}

type CsrfTokenResponse = {
  csrf_token: string;
};

const authEndpoints = ["/auth/login", "/auth/register", "/auth/logout", "/auth/csrf", "/auth/me"];
let csrfTokenPromise: Promise<string> | null = null;

/**
 * Determine whether a request targets an authentication endpoint.
 *
 * @param {string | undefined} url - The request URL.
 * @returns {boolean} Whether the URL is an authentication endpoint.
 */
function isAuthRequest(url: string | undefined): boolean {
  const requestPath = url?.split("?")[0] ?? "";
  return authEndpoints.some((endpoint) => requestPath.endsWith(endpoint));
}

/**
 * Retrieve and cache the in-memory CSRF token.
 *
 * @returns {Promise<string>} The signed CSRF token.
 */
function getCsrfToken(): Promise<string> {
  if (!csrfTokenPromise) {
    csrfTokenPromise = client
      .get<CsrfTokenResponse>("/auth/csrf")
      .then(({ data }) => data.csrf_token)
      .catch((error: unknown) => {
        csrfTokenPromise = null;
        throw error;
      });
  }

  return csrfTokenPromise;
}

/**
 * Check whether a response indicates that the cached CSRF token expired.
 *
 * @param {unknown} data - The error response body.
 * @returns {boolean} Whether the response reports a CSRF validation failure.
 */
function isCsrfValidationError(data: unknown): boolean {
  return (
    typeof data === "object" &&
    data !== null &&
    "detail" in data &&
    data.detail === "Missing or invalid CSRF token"
  );
}

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Add CSRF token to non-GET requests and handle authentication errors.
 */
client.interceptors.request.use(
  async (config) => {
    config.withCredentials = true;
    const method = config.method?.toUpperCase() ?? "GET";
    if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
      config.headers["X-CSRF-Token"] = await getCsrfToken();
    }
    return config;
  },
  (error: unknown) => Promise.reject(error)
);

/**
 * Redirect to login after an unauthorized protected request.
 *
 * @param {AxiosResponse} response - The successful response.
 * @returns {AxiosResponse} The unchanged response.
 */
client.interceptors.response.use(
  (response: AxiosResponse): AxiosResponse => response,
  (error: AxiosError): Promise<AxiosResponse> => {
    if (
      error.response?.status === 403 &&
      isCsrfValidationError(error.response.data) &&
      error.config &&
      !error.config.csrfRetry
    ) {
      csrfTokenPromise = null;
      error.config.csrfRetry = true;
      return client.request(error.config);
    }

    if (error.response?.status === 401 && !isAuthRequest(error.config?.url)) {
      window.location.href = "/login";
    }

    return Promise.reject(error);
  }
);

export default client;
