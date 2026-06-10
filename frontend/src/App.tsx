import { Route, Routes } from 'react-router-dom';
import './App.css';

import HomePage from './core/HomePage';
import BasePage from './core/BasePage';

/**
 * App component handles routing of application.
 */
function App() {
  return (
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
  );
}

export default App;