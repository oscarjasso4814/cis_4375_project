import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";
import { fileURLToPath, URL } from "url";

export default defineConfig({
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      process: "process/browser",
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:5000", // Your Flask backend
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
