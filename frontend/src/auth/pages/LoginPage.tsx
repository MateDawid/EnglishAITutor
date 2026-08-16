import { useEffect, type JSX } from 'react';
import { Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { getAccessTokenFromApi, type LoginFormData } from '../services/LoginService';
import { useForm } from 'react-hook-form';
import { useAlertContext } from '../../core/store/AlertContext';
import { StyledAlert, StyledAppTitleTypography, StyledAvatar, StyledButton, StyledForm, StyledPageTitleTypography, StyledPaper, StyledRedirectTypography, StyledTextField } from './styles';
import { navigateToHomeIfToken } from './utils';


/**
 * Renders the login page.
 *
 * @returns JSX.Element representing the login page.
 */
function LoginPage(): JSX.Element {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>();
  const navigate = useNavigate();
  const { alert, setAlert } = useAlertContext();

  useEffect(() => {
    document.title = 'English AI Tutor - Login';
    setAlert(null);
  }, []);

  useEffect(() => {
    navigateToHomeIfToken(navigate);
  }, [navigate]);

  /**
   * Handles log in on form submission.
   * 
   * @param {LoginFormData} formData - Object containing email and password.
   * @return {Promise<void>} - Promise that resolves when login process is complete.
   */
  const handleLogIn = async (formData: LoginFormData) => {
    getAccessTokenFromApi(formData).then((token) => {
      if (token) {
        setAlert(null);
        navigate('/');
      } else {
        setAlert({ type: 'error', message: 'Invalid email or password.' });
      }
    });
  };

  return (
    <Container component="main" maxWidth="xs">
      <StyledPaper elevation={10}>
        <StyledAppTitleTypography variant="h6">
          English AI Tutor
        </StyledAppTitleTypography>
        <StyledAvatar>
          <LockOutlinedIcon />
        </StyledAvatar>
        <StyledPageTitleTypography variant="h5">
          Log in
        </StyledPageTitleTypography>
        {alert && (
          <StyledAlert
            severity={alert.type}
            onClose={() => setAlert(null)}
          >
            {alert.message}
          </StyledAlert>
        )}
        <StyledForm
          onSubmit={handleSubmit(handleLogIn)}
          noValidate
        >
          <StyledTextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="Email Address"
            autoComplete="username"
            autoFocus
            {...register('username', {
              required: 'Email is required',
            })}
            error={!!errors.username}
            helperText={errors.username ? errors.username.message : ''}
          />
          <StyledTextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="Password"
            type="password"
            autoComplete="current-password"
            {...register('password', {
              required: 'Password is required',
            })}
            error={!!errors.password}
            helperText={errors.password ? errors.password.message : ''}
          />
          <StyledButton
            type="submit"
            variant="contained"
            fullWidth
          >
            Log in
          </StyledButton>
        </StyledForm>
        <StyledRedirectTypography variant="body2">
          No account?
        </StyledRedirectTypography>
        <StyledButton
          type="button"
          onClick={() => navigate('/register')}
          variant="contained"
          fullWidth
        >
          Register
        </StyledButton>
      </StyledPaper>
    </Container>
  );
}

export default LoginPage;