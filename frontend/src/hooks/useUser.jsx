import { useQuery } from '@tanstack/react-query';
import apiClient from '../api'; // Your existing axios instance

export const useUser = () => {
  const token = localStorage.getItem('accessToken');

  return useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      const { data } = await apiClient.get('/auth/me/'); // Or your specific endpoint
      return data;
    },
    enabled: !!token, // don't block access to public pages when not logged in
    // (the header tries to load the user in any case, but this query won't run without a token)
    retry: false, // Don't retry if 401/403 (apiClient handles refresh already)
    refetchOnWindowFocus: false,
    staleTime: 1000 * 60 * 5, // Cache user data for 5 mins
  });
};