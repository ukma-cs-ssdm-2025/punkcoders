// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // Add this block for Docker development
  server: {
    host: '0.0.0.0', // Listen on all network interfaces
    port: 5173,      // Default Vite port
    // Optional: Enable polling if HMR isn't working reliably with Docker volumes
    watch: {
      usePolling: true,
    }
  }
})