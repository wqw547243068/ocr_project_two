import { defineConfig } from 'vite'
import path from 'path'
import { vitePluginForArco } from '@arco-plugins/vite-react'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), vitePluginForArco({
      style: true,
      modifyVars: {
        'border-radius-small': '6px',
        // 'arcoblue-6': '#f85959', //#CF5659, green#88A92F black#021229, green#A7C553 #00AAA6,#009093
        // 'arcoblue-6': '#20A8B7', // 备选
      }
    }),
  ],
  resolve: {
    alias: {
      src: path.resolve(__dirname, './src'),
    },
  },
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
      },
    },
  },
  server: {
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // 后端接口
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    }
  }
})
