import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Navbar } from './Navbar';

describe('Navbar', () => {
  it('renders the navbar with logo', () => {
    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );
    
    // Check for the header/banner element
    expect(screen.getByRole('banner')).toBeInTheDocument();
    
    // Check for the school icon
    expect(screen.getByTestId('SchoolIcon')).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );
    
    expect(screen.getByRole('button', { name: /flashcards/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^chat$/i })).toBeInTheDocument();
  });

  it('renders logout button', () => {
    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );
    
    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument();
  });
});
