import { useEffect, useState } from "react";
import { StyledDivider, StyledPaper, StyledTypography } from "../../styles";
import { StyledHomePageBox } from "./HomePage.styles";
import Button from "@mui/material/Button";
import { LearningSessionModal } from "../../flashcards/components/Modals";

/**
 * HomePage component displays home page of application.
 */
export function HomePage() {
  useEffect(() => {
    document.title = 'English AI Tutor';
  }, []);
  const [learningSessionOpened, setLearningSessionOpened] = useState(false);

  return (
    <StyledHomePageBox>
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
    </StyledHomePageBox>
  );
}
