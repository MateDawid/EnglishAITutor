import { Outlet, useNavigate } from 'react-router-dom';
import { StyledMainBox } from './BasePage.styles';
import { Navbar } from '../components/Navbar';
import { isAuthenticated } from '../../auth/services/LoginService';
import { useEffect } from 'react';
import { Alert, Snackbar } from '@mui/material';
import { useAlertContext } from '../store/AlertContext';

export function BasePage() {
  const { alert, setAlert } = useAlertContext();
  const navigate = useNavigate();

  useEffect(() => {
    let active = true;
    isAuthenticated()
      .then((authenticated) => {
        if (active && !authenticated) {
          navigate('/login', { replace: true });
        }
      })
      .catch(() => {
        if (active) {
          setAlert({ type: 'error', message: 'Unable to verify your session. Please try again.' });
        }
      });

    return () => {
      active = false;
    };
  }, [navigate, setAlert]);

  return (
    <>
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
    </>
  );
}