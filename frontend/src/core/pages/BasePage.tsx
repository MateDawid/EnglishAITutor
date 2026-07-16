import { Outlet, useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import { StyledMainBox } from './BasePage.styles';
import { Navbar } from '../components/Navbar';
import { getAccessTokenFromLocalStorage } from '../../auth/services/LoginService';
import { useEffect } from 'react';
import { Alert, Snackbar } from '@mui/material';
import { useAlertContext } from '../store/AlertContext';

export function BasePage() {
  const { alert, setAlert } = useAlertContext();
  const navigate = useNavigate();

  useEffect(() => {
    /**
     * Asynchronously obtains access token. If token does not exist, navigates to login page.
     */
    const checkIfTokenExists = async () => {
      getAccessTokenFromLocalStorage().then((token) => {
        if (!token) {
          navigate('/login');
        }
      });
    };
    checkIfTokenExists();
  }, [navigate]);

  return (
    <Box>
      <Navbar />
      <StyledMainBox component="main">
        <Outlet />
      </StyledMainBox>
      <Snackbar
        open={!!alert}
        autoHideDuration={8000}
        onClose={() => setAlert(null)}
      >
        <Alert severity={alert?.type} variant="filled" sx={{ width: '100%' }}>
          {alert?.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}