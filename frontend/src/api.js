import axios from 'axios';
import { toast } from 'react-toastify'; 

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/';
const VERSION = 'v0';

const apiClient = axios.create({
  baseURL: API_URL + VERSION,
  timeout: 10000, 
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    throw error;
  }
);

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      console.log("Access token expired, attempting to refresh...");

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await axios.post(API_URL + 'token/refresh/', {
          refresh: refreshToken
        }, {
          timeout: 5000 
        });

        const newAccessToken = response.data.access;
        localStorage.setItem('accessToken', newAccessToken);

        apiClient.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

        return apiClient(originalRequest);

      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
        
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        
        toast.error("Ваша сесія закінчилася. Будь ласка, увійдіть знову.");

        setTimeout(() => {
          globalThis.location.href = '/login';
        }, 2000); 

        throw refreshError;
      }
    }

    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      toast.error("Сервер не відповідає. Будь ласка, спробуйте пізніше.");
    }
    
    throw error;
  }
);

export default apiClient;
export { API_URL };