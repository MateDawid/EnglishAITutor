import { Route, Routes } from 'react-router-dom';
import './App.css';
import ChatPage from './chat/pages/ChatPage';

import { ThemeProvider } from '@mui/material/styles';
import { BasePage, HomePage } from './core/pages';
import FlashcardsPage from './flashcards/pages/FlashcardsPage';
import { theme } from './core/theme';
import LoginPage from './auth/pages/LoginPage';
import RegisterPage from './auth/pages/RegisterPage';
import { AlertProvider } from './core/store/AlertContext';


/**
 * App component handles routing of application.
 */
function App() {
  return (
    <ThemeProvider theme={theme}>
      <AlertProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<BasePage />}>
            <Route
              index
              element={<HomePage />}
            />
            <Route path="flashcards" element={<FlashcardsPage />} />
            <Route path="chat*" element={<ChatPage />} />
            <Route path="*" element={<div>404 Not Found</div>} />

          </Route>
        </Routes>
      </AlertProvider>
    </ThemeProvider>

  );
}

export default App;