import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import type { UIEventHandler } from 'react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const { getMock, setAlertMock } = vi.hoisted(() => ({
  getMock: vi.fn(),
  setAlertMock: vi.fn(),
}));

vi.mock('../../core/apiClient', () => ({
  default: { get: getMock },
}));

vi.mock('../../core/store/AlertContext', () => ({
  useAlertContext: () => ({ setAlert: setAlertMock }),
}));

type MockChatBoxProps = {
  conversations: { id: string; title?: string }[];
  slotProps?: {
    conversationList?: {
      slotProps?: {
        viewport?: {
          onScroll?: UIEventHandler<HTMLDivElement>;
        };
      };
    };
  };
};

vi.mock('@mui/x-chat', () => ({
  createEchoAdapter: () => ({}),
  ChatBox: ({ conversations, slotProps }: MockChatBoxProps) => (
    <div
      role="region"
      aria-label="Conversation list"
      onScroll={slotProps?.conversationList?.slotProps?.viewport?.onScroll}
    >
      <ul>
        {conversations.map((conversation) => (
          <li key={conversation.id}>{conversation.title}</li>
        ))}
      </ul>
    </div>
  ),
}));

import ChatPage from './ChatPage';

describe('ChatPage', () => {
  const originalInnerHeight = window.innerHeight;

  beforeEach(() => {
    vi.clearAllMocks();
    Object.defineProperty(window, 'innerHeight', { configurable: true, value: 624 });
  });

  afterEach(() => {
    Object.defineProperty(window, 'innerHeight', { configurable: true, value: originalInnerHeight });
  });

  it('loads the first conversations page from the API', async () => {
    // GIVEN: The API returns a first page of conversations.
    getMock.mockResolvedValueOnce({
      data: {
        items: [{ id: 'conversation-1', title: 'First lesson' }],
        has_next: false,
      },
    });

    // WHEN: The chat page is rendered.
    render(<ChatPage />);

    // THEN: The conversation is shown and the first page is requested.
    expect(await screen.findByText('First lesson')).toBeInTheDocument();
    expect(getMock).toHaveBeenCalledWith('/conversations', {
      params: { page: 1, page_size: 10 },
    });
  });

  it('loads and appends the next page when the conversation list is scrolled near the bottom', async () => {
    // GIVEN: The API has another conversation page available.
    getMock
      .mockResolvedValueOnce({
        data: {
          items: [{ id: 'conversation-1', title: 'First lesson' }],
          has_next: true,
        },
      })
      .mockResolvedValueOnce({
        data: {
          items: [{ id: 'conversation-2', title: 'Second lesson' }],
          has_next: false,
        },
      });

    render(<ChatPage />);
    expect(await screen.findByText('First lesson')).toBeInTheDocument();

    // WHEN: The conversation list is scrolled near its bottom.
    const conversationList = screen.getByRole('region', { name: 'Conversation list' });
    Object.defineProperties(conversationList, {
      scrollHeight: { configurable: true, value: 500 },
      scrollTop: { configurable: true, value: 421 },
      clientHeight: { configurable: true, value: 100 },
    });
    fireEvent.scroll(conversationList);

    // THEN: The next page is requested and appended to the list.
    expect(await screen.findByText('Second lesson')).toBeInTheDocument();
    expect(getMock).toHaveBeenNthCalledWith(2, '/conversations', {
      params: { page: 2, page_size: 10 },
    });
  });

  it('shows an error when the initial conversations request fails', async () => {
    // GIVEN: The initial API request fails.
    getMock.mockRejectedValueOnce(new Error('Network error'));

    // WHEN: The chat page is rendered.
    render(<ChatPage />);

    // THEN: The user sees an error message.
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Unable to load conversations. Please try again later.'
    );
  });

  it('notifies the user when loading another page fails', async () => {
    // GIVEN: The first page loads but the next-page request fails.
    getMock
      .mockResolvedValueOnce({
        data: {
          items: [{ id: 'conversation-1', title: 'First lesson' }],
          has_next: true,
        },
      })
      .mockRejectedValueOnce(new Error('Network error'));

    render(<ChatPage />);
    expect(await screen.findByText('First lesson')).toBeInTheDocument();

    // WHEN: The conversation list is scrolled near its bottom.
    const conversationList = screen.getByRole('region', { name: 'Conversation list' });
    Object.defineProperties(conversationList, {
      scrollHeight: { configurable: true, value: 500 },
      scrollTop: { configurable: true, value: 421 },
      clientHeight: { configurable: true, value: 100 },
    });
    fireEvent.scroll(conversationList);

    // THEN: The user is notified that more conversations could not be loaded.
    await waitFor(() => {
      expect(setAlertMock).toHaveBeenCalledWith({
        type: 'error',
        message: 'Unable to load more conversations. Please try again.',
      });
    });
  });
});
