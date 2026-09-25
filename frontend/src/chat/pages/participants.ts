import type { ChatUser } from '@mui/x-chat/core';


const UserRole = 'user';
const AssistantRole = 'assistant';

export const User: ChatUser = {
  id: 'user',
  displayName: 'You',
  role: UserRole,
  avatarUrl: '/avatars/user.svg',
};

export const Tutor: ChatUser = {
  id: 'tutor',
  displayName: 'Tutor',
  role: AssistantRole,
  avatarUrl: '/avatars/tutor.svg',
};