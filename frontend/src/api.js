// src/apiClient.js

import axios from 'axios';

// 1. Create the base axios instance
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v0/'
});

// 2. The "Request" Interceptor
// This code runs BEFORE any request is sent
apiClient.interceptors.request.use(
  (config) => {
    // Get the access token from localStorage
    const token = localStorage.getItem('accessToken');
    if (token) {
      // If the token exists, add it to the Authorization header
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Handle any request errors
    return Promise.reject(error);
  }
);

// 3. The "Response" Interceptor
// This code runs AFTER a response is received, but ONLY if there's an error
apiClient.interceptors.response.use(
  (response) => {
    // If the request was successful (status 2xx), just return the response
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // 4. Check for the specific error: 401 (Unauthorized)
    // We also check for `!originalRequest._retry` to prevent infinite loops
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Mark this request as having been retried

      console.log("Access token expired, attempting to refresh...");

      try {
        // 5. Try to get a new access token using the refresh token
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        // Make the refresh request using a NEW, separate axios instance
        // to avoid this interceptor catching its own errors
        const response = await axios.post('http://localhost:8000/api/token/refresh/', {
          refresh: refreshToken
        });

        // 6. SUCCESS: We got a new access token
        const newAccessToken = response.data.access;
        localStorage.setItem('accessToken', newAccessToken);

        // 7. Update the original request's header with the new token
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

        // 8. Retry the original request with the new token
        return apiClient(originalRequest);

      } catch (refreshError) {
        // 9. FAILURE: The refresh token is also expired or invalid
        console.error("Token refresh failed:", refreshError);
        
        // Log the user out
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        
        // Redirect to login page.
        // We use window.location to force a full page reload, clearing all app state.
        window.location.href = '/login';

        return Promise.reject(refreshError);
      }
    }

    // For any other error (like 404, 500), just let it fail
    return Promise.reject(error);
  }
);

export default apiClient;