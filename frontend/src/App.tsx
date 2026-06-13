import { Route, Routes } from 'react-router-dom';
import './App.css';

import { ThemeProvider } from '@mui/material/styles';
import { createTheme } from '@mui/material/styles';
import { BasePage, HomePage } from './core/pages';

const theme = createTheme({
  palette: {
    primary: {
      main: "#222222",
    },
    secondary: {
      main: "#7b0c85",
    }
  }
});

/**
 * App component handles routing of application.
 */
function App() {
  return (
    <ThemeProvider theme={theme}>
      <Routes>
      <Route path="/" element={<BasePage />}>
        <Route
          index
          element={
            <HomePage />
          }
        />
      </Route>
    </Routes>
  </ThemeProvider>

  );
}

export default App;