import { Typography, Avatar, Alert, Button, TextField, Paper, Box, type BoxProps } from '@mui/material';
import { styled } from '@mui/material/styles';

export const StyledPaper = styled(Paper)({
    marginTop: 24, 
    padding: 24
})

export const StyledAppTitleTypography = styled(Typography)({
    textDecoration: 'none',
    fontFamily: 'monospace',
    fontWeight: 700,
    letterSpacing: '.3rem',
    color: 'inherit',
    textAlign: 'center',
    width: '100%',
    marginBottom: 12,
});

export const StyledPageTitleTypography = styled(Typography)({
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
});


export const StyledButton= styled(Button)(({ theme }) => ({
    marginTop: 12,
    backgroundColor: theme.palette.primary.main,
}));