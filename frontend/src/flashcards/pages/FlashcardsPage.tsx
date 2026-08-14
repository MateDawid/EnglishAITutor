
import { StyledTypography } from './FlashcardsPage.styles';
import FlashcardsDataGrid from '../components/FlashcardsDataGrid';
import { StyledPaper } from './FlashcardsPage.styles';
import { Divider } from '@mui/material';

/**
 * FlashcardsPage component to display list of Flashcards and manage flashcard-related actions.
 */
export default function FlashcardsPage() {
  document.title = 'Flashcards';

  return (
    <StyledPaper elevation={24}>
      <StyledTypography variant="h4" gutterBottom>
        Flashcards
      </StyledTypography>
      <Divider sx={{ marginBottom: 2, backgroundColor: '#1f1f1f', height: '3px' }} />
      <FlashcardsDataGrid />
    </StyledPaper>
  );
}
