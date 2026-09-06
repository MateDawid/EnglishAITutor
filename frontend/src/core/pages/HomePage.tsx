import { useEffect } from "react";
import Box from "@mui/material/Box";
import { StyledDivider, StyledPaper, StyledTypography } from "../../styles";

/**
 * HomePage component displays home page of application.
 */
export function HomePage() {
  useEffect(() => {
    document.title = 'English AI Tutor';
  }, []);

  return (
    <Box sx={{ 
      display: "flex", 
      flexDirection: "row", 
      alignItems: "flex-start", 
      justifyContent: "flex-start",
      spacing: 2,
      width: "100%",
    }}>
      <StyledPaper elevation={24}>
        <StyledTypography variant="h4" gutterBottom>
          Learned words
        </StyledTypography>
        <StyledDivider />
        ... statistics about learned words ...
      </StyledPaper>
      <StyledPaper elevation={24}>
        <StyledTypography variant="h4" gutterBottom>
          Learning sessions
        </StyledTypography>
        <StyledDivider />
        ... statistics about learning sessions ...
                <StyledDivider />

        ... button to start a new learning session ...
      </StyledPaper>
    </Box>

  );
}
