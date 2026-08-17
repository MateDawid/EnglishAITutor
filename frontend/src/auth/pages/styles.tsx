import { Typography, Avatar, Alert, Button, TextField, Paper } from '@mui/material';
import { styled } from '@mui/material/styles';
import { theme } from '../../core/theme';

export const StyledPaper = styled(Paper)(({ theme }) => ({
    marginTop: 24,
    padding: 24,
    border: `3px solid ${theme.palette.primary.dark}`,
    borderRadius: 0,
    boxShadow: `3px 3px 0 ${theme.palette.primary.dark}`,
}));

export const StyledAppTitleTypography = styled(Typography)({
    fontFamily: '"Arial Black", sans-serif !important',
    fontWeight: 'normal !important',
    textAlign: 'center',
    width: '100%',
    marginBottom: 12,
});

export const StyledPageTitleTypography = styled(Typography)({
    fontFamily: '"Arial Black", sans-serif !important',
    fontWeight: 'normal !important',
    textAlign: 'center'
});

export const StyledRedirectTypography = styled(Typography)({
    fontFamily: '"Arial", sans-serif !important',

    marginTop: 12,
    textAlign: 'center'
});

export const StyledAvatar = styled(Avatar)(({ theme }) => ({
    marginLeft: 'auto',
    marginRight: 'auto',
    backgroundColor: theme.palette.primary.main,
    textAlign: 'center',
    marginBottom: 12,
}));

export const StyledAlert = styled(Alert)({
    marginTop: 12,
    whiteSpace: 'pre-wrap'
});

export const StyledForm = styled("form")({
    marginTop: 12,
});

export const StyledTextField = styled(TextField)({
    margin: 0,
    marginTop: 12,
    '& .MuiOutlinedInput-root': {
        borderRadius: 0,
        borderColor: `${theme.palette.primary.dark} !important`,
        boxShadow: `1px 1px 0 ${theme.palette.primary.dark}`,
    },
    '& .MuiOutlinedInput-root:hover': {
        borderRadius: 0,
        boxShadow: `2px 2px 0 ${theme.palette.primary.dark}`,
    },
    '& .MuiOutlinedInput-root.Mui-focused': {
        borderRadius: 0,
        boxShadow: `3px 3px 0 ${theme.palette.primary.dark}`,
    },
    '& .MuiInputBase-input, .MuiInputLabel-root, .MuiFormHelperText-root': {
        fontFamily: '"Arial", sans-serif',
        color: theme.palette.primary.dark,
    },

    '& .MuiInputLabel-root': {
        fontWeight: 'bold',
    },
});

export const StyledButton = styled(Button)(({ theme }) => ({
    marginTop: 12,
    backgroundColor: theme.palette.primary.main,
    borderRadius: 0,
    boxShadow: 'none',
    fontFamily: '"Arial Black", sans-serif !important',
    fontWeight: 'normal !important',
    fontSize: '14px !important',
    '&:hover': {
        boxShadow: 'none',
    },
}));