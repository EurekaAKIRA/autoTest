import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        ws: true,
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('proxy error', err)
          })
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Sending Request:', {
              method: req.method,
              url: req.url,
              headers: proxyReq.getHeaders()
            })
          })
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('Received Response:', {
              statusCode: proxyRes.statusCode,
              url: req.url,
              headers: proxyRes.headers
            })
          })
        }
      }
    }
  }
}) 