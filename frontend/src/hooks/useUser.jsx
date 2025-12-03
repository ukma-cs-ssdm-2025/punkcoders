import { useQuery } from '@tanstack/react-query';
import apiClient from '../api'; // Your existing axios instance

export const useUser = () => {
  return useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      const { data } = await apiClient.get('/auth/me/'); // Or your specific endpoint
      return data;
    },
    retry: false, // Don't retry if 401/403 (apiClient handles refresh already)
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60 * 5, // Cache user data for 5 mins
  });
};