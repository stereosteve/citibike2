import { defineConfig } from 'vite'
import reactRefresh from '@vitejs/plugin-react-refresh'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [reactRefresh()],
  server: {
    proxy: {
      '/db': {
        target: 'http://localhost:8123/',
        rewrite: (path) => path.replace(/^\/db/, '')
      }
    }
  }
})
