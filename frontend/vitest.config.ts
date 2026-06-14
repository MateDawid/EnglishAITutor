import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: './testsSetup.ts',
    server: {
      deps: {
        inline: ['@mui/material', '@mui/icons-material', 'react-transition-group'],
      },
    },
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'json-summary', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.config.ts',
        '**/*.d.ts',
      ],
    },
  },
  resolve: {
    mainFields: ['module', 'main'],
    conditions: ['import', 'module', 'browser', 'default'],
  },
});
