
import { StyledTypography, StyledDivider } from '../../styles';
import { FlashcardsDataGrid } from '../components/FlashcardsDataGrid';
import { useEffect } from 'react';
import { FlashcardsPaper } from './FlashcardsPage.styles';

/**
 * FlashcardsPage component to display list of Flashcards and manage flashcard-related actions.
 */
export default function FlashcardsPage() {
  useEffect(() => {
    document.title = 'Flashcards';
  }, []);

  return (
    <FlashcardsPaper elevation={24}>
      <StyledTypography variant="h4" gutterBottom>
        Flashcards
      </StyledTypography>
      <StyledDivider />
      <FlashcardsDataGrid />
    </FlashcardsPaper>
  );
}
