import React from 'react';
import { createRoot } from 'react-dom/client' 
import { BrowserRouter } from 'react-router-dom';
import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query';
import './style.css'
import App from './App.jsx'

// --- React Query Client ---
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: false,
      retry: (failureCount, error) => {
        if (error.response?.status === 404) return false;
        return failureCount < 3;
      },
    },
  },
});

const root = createRoot(document.getElementById('root')); 
root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);