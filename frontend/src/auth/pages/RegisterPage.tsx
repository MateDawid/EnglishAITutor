import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container } from '@mui/material';
import { useForm } from 'react-hook-form';
import AppRegistrationOutlinedIcon from '@mui/icons-material/AppRegistrationOutlined';
import { navigateToHomeIfToken } from './utils';
import { StyledAlert, StyledAppTitleTypography, StyledAvatar, StyledButton, StyledForm, StyledPageTitleTypography, StyledPaper, StyledRedirectTypography, StyledTextField } from './styles';
import { useAlertContext } from '../../core/store/AlertContext';
import { getErrorMessage, registerUser, type ApiErrorResponse, type RegisterFormData } from '../services/RegisterService';


const PASSWORD_VALIDATION_SETUP = {
  required: 'Password is required',
  minLength: {
    value: 8,
    message: 'Password must be at least 8 characters long',
  },
}

const EMAIL_VALIDATION_SETUP = {
  required: 'Email is required',
  pattern: {
    value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    message: 'Invalid email address',
  },
}

/**
 * RegisterPage component handles user registration.
 * It manages the email and password input fields,
 * validates the input, and performs the registration process.
 */
function RegisterPage() {
  const { register, handleSubmit, formState: { errors } } = useForm<RegisterFormData>();
  const navigate = useNavigate();
  const { alert, setAlert } = useAlertContext();

  useEffect(() => {
    document.title = 'English AI Tutor - Register';
  }, []);

  useEffect(() => {
    navigateToHomeIfToken(navigate);
  }, [navigate]);

  /**
   * Handles form submission.
   * Validates input fields and calls API to create user.
   * @param {RegisterFormData} formData - Form data.
   */
  const handleRegister = async (formData: RegisterFormData) => {
    registerUser(formData).then(() => {
      setAlert({ type: 'success', message: 'Registration successful.' });
      navigate('/login');
    }).catch((error: ApiErrorResponse) => {
      setAlert({ type: 'error', message: getErrorMessage(error) });
    });
  };

  return (
    <Container component="main" maxWidth="xs">
      <StyledPaper elevation={10}>
        <StyledAppTitleTypography variant="h6">
          English AI Tutor
        </StyledAppTitleTypography>
        <StyledAvatar>
          <AppRegistrationOutlinedIcon />
        </StyledAvatar>
        <StyledPageTitleTypography variant="h5">
          Register
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
          onSubmit={handleSubmit(handleRegister)}
          noValidate
        >
          <StyledTextField
            data-cy="email-field"
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="Email Address"
            autoComplete="email"
            autoFocus
            {...register('email', EMAIL_VALIDATION_SETUP)}
            error={!!errors.email}
            helperText={errors.email ? errors.email.message : ''}
          />
          <StyledTextField
            data-cy="password-1-field"
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="Password"
            type="password"
            autoComplete="current-password"
            {...register('password_1', PASSWORD_VALIDATION_SETUP)}
            error={!!errors.password_1}
            helperText={errors.password_1 ? errors.password_1.message : ''}
          />
          <StyledTextField
            data-cy="password-2-field"
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="Repeat password"
            type="password"
            autoComplete="current-password"
            {...register('password_2', PASSWORD_VALIDATION_SETUP)}
            error={!!errors.password_2}
            helperText={errors.password_2 ? errors.password_2.message : ''}
          />
          <StyledButton
            type="submit"
            variant="contained"
            fullWidth
          >
            Register
          </StyledButton>
        </StyledForm>
        <StyledRedirectTypography variant="body2">
          Have account already?
        </StyledRedirectTypography>
        <StyledButton
          type="button"
          onClick={() => navigate('/login')}
          variant="contained"
          fullWidth
        >
          Log in
        </StyledButton>
      </StyledPaper>
    </Container>
  );
}

export default RegisterPage;