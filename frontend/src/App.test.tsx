import { describe, it, expect } from 'vitest';

describe('App', () => {
  it('basic test - setup works', () => {
    expect(1 + 1).toBe(2);
  });
  
  it('document is defined', () => {
    expect(document).toBeDefined();
    expect(document.body).toBeDefined();
  });
});
