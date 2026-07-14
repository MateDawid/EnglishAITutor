import { useEffect, type JSX } from 'react';
import { Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { getAccessTokenFromApi, getAccessTokenFromLocalStorage } from '../services/TokenService';
import { useForm } from 'react-hook-form';
import { useAlertContext } from '../../core/store/AlertContext';
import { StyledAlert, StyledAppTitleTypography, StyledAvatar, StyledButton, StyledForm, StyledPageTitleTypography, StyledPaper, StyledTextField } from './styles';

/**
 * Type definition for the login form data.
 */
type LoginFormData = {
  email: string;
  password: string;
};

/**
 * Renders the login page.
 *
 * @returns JSX.Element representing the login page.
 */
function LoginPage(): JSX.Element {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>();
  const navigate = useNavigate();
  const { alert, setAlert } = useAlertContext();

  /**
   * Asynchronously obtains access token. If token exists, navigates to landing page.
   */
  useEffect(() => {
    const checkIfTokenExists = async () => {
      getAccessTokenFromLocalStorage().then((token) => {
        if (token) {
          navigate('/');
        }
      });
    };
    checkIfTokenExists();
  }, []);

  /**
   * Handles log in on form submission.
   * 
   * @param {LoginFormData} formData - Object containing email and password.
   * @return {Promise<void>} - Promise that resolves when login process is complete.
   */
  const handleLogIn = async (formData: LoginFormData) => {
    getAccessTokenFromApi(formData.email, formData.password).then((token) => {
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
            autoComplete="email"
            autoFocus
            {...register('email', {
              required: 'Email is required',
            })}
            error={!!errors.email}
            helperText={errors.email ? errors.email.message : ''}
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