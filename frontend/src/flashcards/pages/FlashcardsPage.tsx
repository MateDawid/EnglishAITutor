
import { FlashcardsDataGrid } from '../components/FlashcardsDataGrid';
import { StyledTypography } from './FlashcardsPage.styles';
import { StyledPaper } from './FlashcardsPage.styles';
import { StyledDivider } from './FlashcardsPage.styles';
import { useEffect } from 'react';

/**
 * FlashcardsPage component to display list of Flashcards and manage flashcard-related actions.
 */
export default function FlashcardsPage() {
  useEffect(() => {
    document.title = 'Flashcards';
  }, []);

  return (
    <StyledPaper elevation={24}>
      <StyledTypography variant="h4" gutterBottom>
        Flashcards
      </StyledTypography>
      <StyledDivider />
      <FlashcardsDataGrid />
    </StyledPaper>
  );
}
