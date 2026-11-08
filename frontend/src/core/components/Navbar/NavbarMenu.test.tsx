import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import NavbarMenu from './NavbarMenu';
import { AlertProvider } from '../../store/AlertContext';
import { logoutUser } from '../../../auth/services/LoginService';

vi.mock('../../../auth/services/LoginService', () => ({
  logoutUser: vi.fn(),
}));

describe('NavbarMenu', () => {
  const renderNavbarMenu = () => {
    return render(
      <BrowserRouter>
        <AlertProvider>
          <NavbarMenu />
        </AlertProvider>
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
    expect(await screen.findByRole('menuitem', { name: /flashcards/i })).toBeVisible();
    expect(await screen.findByRole('menuitem', { name: /^chat$/i })).toBeVisible();
  });

  it('renders all navigation items from navConfig', async () => {
    const user = userEvent.setup();
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    await user.click(menuButton);
    
    // Check for navigation items
    expect(await screen.findByRole('menuitem', { name: /flashcards/i })).toBeInTheDocument();
    expect(await screen.findByRole('menuitem', { name: /^chat$/i })).toBeInTheDocument();
    
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
    
    const flashcardsItem = await screen.findByRole('menuitem', { name: /flashcards/i });
    await user.click(flashcardsItem);
    
    await waitFor(() => {
      expect(screen.queryByRole('menuitem', { name: /^chat$/i })).not.toBeInTheDocument();
    });
  });

  it('logs out through the API when the logout menu item is clicked', async () => {
    const user = userEvent.setup();
    vi.mocked(logoutUser).mockResolvedValue(undefined);
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    await user.click(menuButton);
    
    const logoutItem = screen.getByRole('menuitem', { name: /logout/i });
    await user.click(logoutItem);

    await waitFor(() => {
      expect(logoutUser).toHaveBeenCalledOnce();
    });
  });

  it('navigation items have correct links', async () => {
    const user = userEvent.setup();
    renderNavbarMenu();
    
    const menuButton = screen.getByRole('button');
    await user.click(menuButton);
    
    const flashcardsLink = await screen.findByRole('menuitem', { name: /flashcards/i });
    const chatLink = await screen.findByRole('menuitem', { name: /^chat$/i });
    
    expect(flashcardsLink).toHaveAttribute('href', '/flashcards');
    expect(chatLink).toHaveAttribute('href', '/chat');
  });

  it('passes through additional props to Box component', () => {
    const { container } = render(
      <BrowserRouter>
        <AlertProvider>
          <NavbarMenu data-testid="custom-menu" />
        </AlertProvider>
      </BrowserRouter>
    );
    
    const box = container.querySelector('[data-testid="custom-menu"]');
    expect(box).toBeInTheDocument();
  });

  it('menu is initially closed', () => {
    renderNavbarMenu();
    
    // Menu items should not be visible initially
    expect(screen.queryByRole('menuitem', { name: /flashcards/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('menuitem', { name: /^chat$/i })).not.toBeInTheDocument();
  });
});
