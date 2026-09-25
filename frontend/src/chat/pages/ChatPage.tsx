
import { useEffect, useState } from 'react';
import { ChatBox } from '@mui/x-chat';
import { User, Tutor } from './participants';
import { testInitialConversations, testInitialMessages, testAdapter } from './testData';


/**
 * ChatPage component to display chat interface and manage chat-related actions.
 */
export default function ChatPage() {
  const [activeConversationId, setActiveConversationId] = useState<string | undefined>(undefined);


  useEffect(() => {
    document.title = 'Chat';
  }, []);

  return (
    <ChatBox
      key={activeConversationId}
      adapter={testAdapter}
      currentUser={User}
      members={[User, Tutor]}
      initialConversations={testInitialConversations}
      initialActiveConversationId={activeConversationId}
      initialMessages={testInitialMessages}
      onActiveConversationChange={setActiveConversationId}
      features={{
        conversationList: true,
        conversationHeader: true,
        dateDivider: true,
        attachments: false,
        suggestions: false, 
      }}
      sx={{
        height: 'calc(100vh - 64px)', // Adjust height as needed
      }}
    />
  );
} 
