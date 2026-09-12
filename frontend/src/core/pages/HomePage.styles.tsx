import { Box } from '@mui/material';
import { styled } from '@mui/material/styles';

export const StyledHomePageBox = styled(Box)<{ component?: React.ElementType }>({
    display: "flex", 
    flexDirection: "row", 
    alignItems: "flex-start", 
    justifyContent: "flex-start",
    spacing: 2,
    width: "100%",
});