import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import NavbarMenu from './NavbarMenu';

describe('NavbarMenu', () => {
  const renderNavbarMenu = () => {
    return render(
      <BrowserRouter>
        <NavbarMenu />
      </BrowserRouter>
    );
  };

  it('renders the menu icon button', () => {
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    expect(menuButton).toBeInTheDocument();
  });

  it('opens menu when menu button is clicked', async () => {
    const user = userEvent.setup();
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    await user.click(menuButton);
    
    // Check if menu is open by looking for menu items
    expect(screen.getByText('Flashcards')).toBeVisible();
    expect(screen.getByText('Chat with Tutor')).toBeVisible();
  });

  it('renders all navigation items from navConfig', async () => {
    const user = userEvent.setup();
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    await user.click(menuButton);
    
    // Check for navigation items
    expect(screen.getByText('Flashcards')).toBeInTheDocument();
    expect(screen.getByText('Chat with Tutor')).toBeInTheDocument();
    
    // Check for icons
    expect(screen.getByTestId('StickyNote2Icon')).toBeInTheDocument();
    expect(screen.getByTestId('AssistantIcon')).toBeInTheDocument();
  });

  it('renders logout menu item', async () => {
    const user = userEvent.setup();
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    await user.click(menuButton);
    
    expect(screen.getByText('Logout')).toBeInTheDocument();
    expect(screen.getByTestId('LogoutIcon')).toBeInTheDocument();
  });

  it('closes menu when a navigation item is clicked', async () => {
    const user = userEvent.setup();
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    await user.click(menuButton);
    
    const flashcardsItem = screen.getByText('Flashcards');
    await user.click(flashcardsItem);
    
    await waitFor(() => {
      expect(screen.queryByText('Chat with Tutor')).not.toBeVisible();
    });
  });

  it('handles logout button click', async () => {
    const consoleLogSpy = vi.spyOn(console, 'log');
    const user = userEvent.setup();
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    await user.click(menuButton);
    
    const logoutItem = screen.getByText('Logout');
    await user.click(logoutItem);
    
    expect(consoleLogSpy).toHaveBeenCalledWith('Logout clicked');
    consoleLogSpy.mockRestore();
  });

  it('navigation items have correct links', async () => {
    const user = userEvent.setup();
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    await user.click(menuButton);
    
    const flashcardsLink = screen.getByRole('menuitem', { name: /flashcards/i });
    const chatLink = screen.getByRole('menuitem', { name: /chat with tutor/i });
    
    expect(flashcardsLink).toHaveAttribute('href', '/flashcards');
    expect(chatLink).toHaveAttribute('href', '/chat');
  });

  it('passes through additional props to Box component', () => {
    const { container } = render(
      <BrowserRouter>
        <NavbarMenu data-testid="custom-menu" />
      </BrowserRouter>
    );
    
    const box = container.querySelector('[data-testid="custom-menu"]');
    expect(box).toBeInTheDocument();
  });

  it('menu is initially closed', () => {
    renderNavbarMenu();
    
    // Menu items should not be visible initially
    expect(screen.queryByText('Flashcards')).not.toBeInTheDocument();
    expect(screen.queryByText('Chat with Tutor')).not.toBeInTheDocument();
  });
});
