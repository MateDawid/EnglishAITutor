import { useEffect, useState } from "react";
import { StyledDivider, StyledPaper, StyledTypography } from "../../styles";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import LearningSessionModal from "../../learningSessions/components/LearningSessionModal/LearningSessionModal";

/**
 * HomePage component displays home page of application.
 */
export function HomePage() {
  useEffect(() => {
    document.title = 'English AI Tutor';
  }, []);
  const [learningSessionOpened, setLearningSessionOpened] = useState(false);

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
          Learning sessions
        </StyledTypography>
        <StyledDivider />
        <Button variant="contained" color="primary" onClick={() => setLearningSessionOpened(true)}>
          Start session
        </Button>
      </StyledPaper>
      <LearningSessionModal
        open={learningSessionOpened}
        setOpen={setLearningSessionOpened}
      />
    </Box>
  );
}
