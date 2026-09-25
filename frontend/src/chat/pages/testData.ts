import { createEchoAdapter } from "@mui/x-chat";

import { User, Tutor } from './participants';
import type { ChatRole, ChatMessageStatus, ChatMessage } from '@mui/x-chat/core';

export const testInitialConversations = [
  { id: 'test_id_1', title: 'First lesson', participants: [User, Tutor] },
  { id: 'test_id_2', title: 'Second lesson', participants: [User, Tutor] },
];

export const testInitialMessages: ChatMessage[] = [
  // First lesson - Day 1
  {
    id: 'msg_1',
    conversationId: 'test_id_1',
    role: 'assistant',
    author: Tutor,
    status: 'sent',
    createdAt: new Date('2026-09-20T09:00:00Z'),
    parts: [
      {
        type: 'text',
        text: 'Welcome to the first lesson! Today we will learn React hooks.',
      },
    ],
  },
  {
    id: 'msg_2',
    conversationId: 'test_id_1',
    role: 'user',
    author: User,
    status: 'sent',
    createdAt: new Date('2026-09-20T09:01:30Z'),
    parts: [
      {
        type: 'text',
        text: 'Sounds good. What exactly is a hook?',
      },
    ],
  },
  {
    id: 'msg_3',
    conversationId: 'test_id_1',
    role: 'assistant',
    author: Tutor,
    status: 'sent',
    createdAt: new Date('2026-09-20T09:02:15Z'),
    parts: [
      {
        type: 'text',
        text: 'A hook is a special React function that lets you use state and other React features in function components.',
      },
    ],
  },

  // First lesson - Day 2
  {
    id: 'msg_4',
    conversationId: 'test_id_1',
    role: 'user',
    author: User,
    status: 'sent',
    createdAt: new Date('2026-09-21T10:15:00Z'),
    parts: [
      {
        type: 'text',
        text: 'Can you explain useState?',
      },
    ],
  },
  {
    id: 'msg_5',
    conversationId: 'test_id_1',
    role: 'assistant',
    author: Tutor,
    status: 'sent',
    createdAt: new Date('2026-09-21T10:16:10Z'),
    parts: [
      {
        type: 'text',
        text: 'useState allows a functional component to store and update local state.',
      },
    ],
  },
  {
    id: 'msg_6',
    conversationId: 'test_id_1',
    role: 'assistant',
    author: Tutor,
    status: 'sent',
    createdAt: new Date('2026-09-21T10:17:30Z'),
    parts: [
      {
        type: 'text',
        text: 'For example: const [count, setCount] = useState(0);',
      },
    ],
  },

  // First lesson - Day 3
  {
    id: 'msg_7',
    conversationId: 'test_id_1',
    role: 'user',
    author: User,
    status: 'sent',
    createdAt: new Date('2026-09-24T08:00:00Z'),
    parts: [
      {
        type: 'text',
        text: 'What about useEffect?',
      },
    ],
  },
  {
    id: 'msg_8',
    conversationId: 'test_id_1',
    role: 'assistant',
    author: Tutor,
    status: 'sent',
    createdAt: new Date('2026-09-24T08:01:20Z'),
    parts: [
      {
        type: 'text',
        text: 'useEffect is used for side effects such as API calls, subscriptions, timers, and updating the document title.',
      },
    ],
  },

  // Second lesson
  {
    id: 'msg_9',
    conversationId: 'test_id_2',
    role: 'assistant',
    author: Tutor,
    status: 'sent',
    createdAt: new Date('2026-09-22T12:00:00Z'),
    parts: [
      {
        type: 'text',
        text: 'Welcome to the TypeScript lesson.',
      },
    ],
  },
  {
    id: 'msg_10',
    conversationId: 'test_id_2',
    role: 'user',
    author: User,
    status: 'sent',
    createdAt: new Date('2026-09-22T12:01:10Z'),
    parts: [
      {
        type: 'text',
        text: 'What is the difference between interface and type?',
      },
    ],
  },
  {
    id: 'msg_11',
    conversationId: 'test_id_2',
    role: 'assistant',
    author: Tutor,
    status: 'sent',
    createdAt: new Date('2026-09-22T12:03:00Z'),
    parts: [
      {
        type: 'text',
        text: 'Interfaces are usually preferred for object shapes, while type aliases are more flexible for unions and advanced type operations.',
      },
    ],
  },
  {
    id: 'msg_12',
    conversationId: 'test_id_2',
    role: 'user',
    author: User,
    status: 'sent',
    createdAt: new Date('2026-09-22T12:04:20Z'),
    parts: [
      {
        type: 'text',
        text: 'Can interfaces extend other interfaces?',
      },
    ],
  },
  {
    id: 'msg_13',
    conversationId: 'test_id_2',
    role: 'assistant',
    author: Tutor,
    status: 'sent',
    createdAt: new Date('2026-09-22T12:04:55Z'),
    parts: [
      {
        type: 'text',
        text: 'Yes. Interface inheritance is a common TypeScript pattern.',
      },
    ],
  },
];


export const testAdapter = createEchoAdapter();
