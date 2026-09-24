
import { useEffect, useState } from 'react';
import { ChatBox, createEchoAdapter } from '@mui/x-chat';
import type { ChatUser, ChatConversation, ChatMessage, ChatRole, ChatMessageStatus } from '@mui/x-chat/core';

const UserRole = 'user';
const AssistantRole = 'assistant';

const User: ChatUser = {
  id: 'user',
  displayName: 'You',
  role: UserRole,
  avatarUrl: '/avatars/user.svg',
};

const Tutor: ChatUser = {
  id: 'tutor',
  displayName: 'Tutor',
  role: AssistantRole,
  avatarUrl: '/avatars/tutor.svg',
};


const testInitialConversations = [
  { id: 'test_id_1', title: 'Assistant_1', participants: [User, Tutor]},
  { id: 'test_id_2', title: 'Assistant_2', participants: [User, Tutor]},
];

const testInitialMessages = [
  {
    id: 'welcome',
    conversationId: 'test_id_1',
    role: "assistant" as ChatRole,
        parts: [
      { type: 'text' as ChatMessageStatus, text: 'Hello! Send a message to see a response.' },
    ],
    author: Tutor,
    status: 'sent',
  },
];

const adapter = createEchoAdapter();

/**
 * ChatPage component to display chat interface and manage chat-related actions.
 */
export default function ChatPage() {
  const [initialConversations, setInitialConversations] = useState<ChatConversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | undefined>(undefined);
  const [initialMessages, setInitialMessages] = useState<ChatMessage[]>([]);

  useEffect(() => {
    document.title = 'Chat';
  }, []);

  useEffect(() => {
    // Simulate fetching initial conversations from an API or other source
    const fetchInitialConversations = async () => {
      // TODO: Replace this with your actual data fetching logic
      // const conversations: ChatConversation[] = ...;
      setInitialConversations(testInitialConversations);
      setActiveConversationId(testInitialConversations[0].id); // Set the first conversation as active
      setInitialMessages(testInitialMessages); // Set initial messages for the active conversation
    };
    fetchInitialConversations();
  }, []);

  return (
    <ChatBox
      adapter={adapter}
      currentUser={User}
      members={[User, Tutor]}
      initialConversations={initialConversations}
      initialActiveConversationId={activeConversationId}
      initialMessages={initialMessages}
      // onActiveConversationChange={setActiveConversationId}
      // variant={variant}
      // density={density}
      // layoutMode={layoutMode}
      // suggestions={sampleSuggestions}
      // suggestionsAutoSubmit={suggestionsAutoSubmit}
      features={{
        conversationList: true, // show the conversation sidebar / drawer (default false)
        // conversationHeader: true, // show the title, subtitle, and actions bar (default true)
        // dateDivider: true, // show date separators between calendar days (default false)
        // unreadMarker: true, // show the "new messages" marker (default false)
        // attachments: false, // disable attachment functionality (default true)
        // helperText: false, // hide the helper text below the composer (default true)
        // scrollToBottom: false, // disable the scroll-to-bottom affordance (default true)
        // autoScroll: { buffer: 300 }, // custom auto-scroll threshold (default true)
        // suggestions: false, // hide prompt suggestions in the empty state (default true)
      }}
      // sx={outerSx}
      sx={{
        height: 'calc(100vh - 64px)', // Adjust height as needed
        // border: '1px solid',
        // borderColor: 'divider',
        // borderRadius: 1,
      }}
    />
  );
} 
