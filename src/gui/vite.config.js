import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify';
import path from 'path'

export default defineConfig({
  server: {
     host: "0.0.0.0",
     port: 8081
  },
  resolve: {
    alias: {
      vue: '@vue/compat',
      '@': path.resolve(__dirname, './src'),
    }
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          compatConfig: {
            MODE: 2
          }
        }
      }
    }),
    vuetify({ autoImport: true })
  ],
  build: {
    rollupOptions: {
      // https://rollupjs.org/guide/en/#outputmanualchunks
      output: {
        manualChunks: {
          vue: ['vue', 'vue-router'],
          vuetify: [
            'vuetify',
            'vuetify/components',
            'vuetify/directives',
          ],
          materialdesignicons: ['@mdi/font/css/materialdesignicons.css'],
        },
      },
    },
  },
})
