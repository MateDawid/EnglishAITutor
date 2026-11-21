
import { Alert, CircularProgress } from '@mui/material';
import { ChatBox } from '@mui/x-chat';
import type { ChatConversation } from '@mui/x-chat/core';
import { useEffect, useRef, useState, type UIEvent } from 'react';
import { User, Tutor } from './participants';
import { testAdapter } from './testData';
import client from '../../core/apiClient';
import { useAlertContext } from '../../core/store/AlertContext';

const CHAT_PAGE_TOP_OFFSET_PX = 64;
const CONVERSATION_ROW_HEIGHT_PX = 56;
const CONVERSATION_PREFETCH_THRESHOLD_PX = 80;
const MAX_CONVERSATION_PAGE_SIZE = 50;

type ConversationListResponse = {
  items: {
    id: string;
    title: string;
  }[];
  has_next: boolean;
};

type ConversationState =
  | { status: 'loading' }
  | { status: 'loaded'; conversations: ChatConversation[]; page: number; hasNextPage: boolean }
  | { status: 'error' };

/**
 * ChatPage component to display chat interface and manage chat-related actions.
 */
export default function ChatPage() {
  const [activeConversationId, setActiveConversationId] = useState<string | undefined>(undefined);
  const [pageSize] = useState(getConversationPageSize);
  const [conversationState, setConversationState] = useState<ConversationState>({ status: 'loading' });
  const isMounted = useRef(false);
  const isLoadingMore = useRef(false);
  const { setAlert } = useAlertContext();

  useEffect(() => {
    document.title = 'Chat';
  }, []);

  useEffect(() => {
    isMounted.current = true;

    /**
     * Load the first page of conversations.
     *
     * @returns {Promise<void>} A promise that resolves when conversations are loaded.
     */
    async function loadConversations(): Promise<void> {
      try {
        const { data } = await client.get<ConversationListResponse>('/conversations', {
          params: { page: 1, page_size: pageSize },
        });

        if (isMounted.current) {
          setConversationState({
            status: 'loaded',
            conversations: toChatConversations(data.items),
            page: 1,
            hasNextPage: data.has_next,
          });
        }
      } catch {
        if (isMounted.current) {
          setConversationState({ status: 'error' });
        }
      }
    }

    void loadConversations();
    return () => {
      isMounted.current = false;
    };
  }, [pageSize]);

  /**
   * Load the next conversations page when the list is scrolled near its bottom.
   *
   * @returns {Promise<void>} A promise that resolves when the page is loaded.
   */
  async function loadMoreConversations(): Promise<void> {
    if (conversationState.status !== 'loaded' || !conversationState.hasNextPage || isLoadingMore.current) {
      return;
    }

    isLoadingMore.current = true;
    const nextPage = conversationState.page + 1;
    try {
      const { data } = await client.get<ConversationListResponse>('/conversations', {
        params: { page: nextPage, page_size: pageSize },
      });

      if (isMounted.current) {
        setConversationState((current) =>
          current.status === 'loaded'
            ? {
                ...current,
                conversations: [...current.conversations, ...toChatConversations(data.items)],
                page: nextPage,
                hasNextPage: data.has_next,
              }
            : current
        );
      }
    } catch {
      if (isMounted.current) {
        setAlert({ type: 'error', message: 'Unable to load more conversations. Please try again.' });
      }
    } finally {
      isLoadingMore.current = false;
    }
  }

  /**
   * Request another page when the conversation list approaches its bottom.
   *
   * @param {UIEvent<HTMLDivElement>} event - The conversation list scroll event.
   */
  function handleConversationListScroll(event: UIEvent<HTMLDivElement>): void {
    const { scrollHeight, scrollTop, clientHeight } = event.currentTarget;
    if (scrollHeight - scrollTop - clientHeight < CONVERSATION_PREFETCH_THRESHOLD_PX) {
      void loadMoreConversations();
    }
  }

  if (conversationState.status === 'loading') {
    return <CircularProgress aria-label="Loading conversations" />;
  }

  if (conversationState.status === 'error') {
    return <Alert severity="error">Unable to load conversations. Please try again later.</Alert>;
  }

  return (
    <ChatBox
      key={activeConversationId}
      adapter={testAdapter}
      currentUser={User}
      members={[User, Tutor]}
      conversations={conversationState.conversations}
      onConversationsChange={(conversations) =>
        setConversationState((current) =>
          current.status === 'loaded' ? { ...current, conversations } : current
        )
      }
      initialActiveConversationId={activeConversationId}
      onActiveConversationChange={setActiveConversationId}
      slotProps={{
        conversationList: {
          slotProps: {
            viewport: { onScroll: handleConversationListScroll },
          },
        },
      }}
      features={{
        conversationList: true,
        conversationHeader: true,
        dateDivider: true,
        attachments: false,
        suggestions: false, 
      }}
      sx={{
        height: `calc(100vh - ${CHAT_PAGE_TOP_OFFSET_PX}px)`,
      }}
    />
  );
} 

/**
 * Convert API conversation items to the chat component's conversation shape.
 *
 * @param {ConversationListResponse['items']} items - The API conversation items.
 * @returns {ChatConversation[]} The mapped conversations.
 */
function toChatConversations(items: ConversationListResponse['items']): ChatConversation[] {
  return items.map(({ id, title }) => ({
    id,
    title,
    participants: [User, Tutor],
  }));
}

/**
 * Estimate a page size that fills the visible conversation list.
 *
 * @returns {number} A page size between one and the API's maximum.
 */
function getConversationPageSize(): number {
  const listHeight = Math.max(CONVERSATION_ROW_HEIGHT_PX, window.innerHeight - CHAT_PAGE_TOP_OFFSET_PX);
  return Math.min(MAX_CONVERSATION_PAGE_SIZE, Math.max(1, Math.ceil(listHeight / CONVERSATION_ROW_HEIGHT_PX)));
}
