import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';

// Polyfill for document.styleSheets (required for @emotion)
class MockStyleSheet {
  cssRules: CSSRule[] = [];
  insertRule() {
    return 0;
  }
  deleteRule() {}
}

if (!document.styleSheets || !('insertRule' in (document.styleSheets[0] || {}))) {
  Object.defineProperty(document, 'styleSheets', {
    value: [],
    writable: true,
  });
}

// @ts-expect-error - Polyfilling CSSStyleSheet for test environment
if (typeof window.CSSStyleSheet === 'undefined' || !window.CSSStyleSheet.prototype.insertRule) {
  // @ts-expect-error - Assigning mock implementation
  window.CSSStyleSheet = MockStyleSheet;
  // @ts-expect-error - Assigning mock implementation
  global.CSSStyleSheet = MockStyleSheet;
}

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: () => {}, // deprecated
    removeListener: () => {}, // deprecated
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => {},
  }),
});

// Cleanup after each test
afterEach(() => {
  cleanup();
});
