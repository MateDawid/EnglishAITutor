import { BrowserRouter } from 'react-router-dom';
import App from './App';
import axios from 'axios';
import { createRoot } from 'react-dom/client';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);