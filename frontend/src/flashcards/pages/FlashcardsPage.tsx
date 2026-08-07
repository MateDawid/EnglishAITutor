
import { Paper } from '@mui/material';
import FlashcardsDataGrid from '../components/FlashcardsDataGrid';


/**
 * FlashcardsPage component to display list of Flashcards and manage flashcard-related actions.
 */
export default function FlashcardsPage() {
  document.title = 'Flashcards';

  return (
    <Paper elevation={24} sx={{ padding: 2, bgColor: '#F1F1F1', margin: 2 }}>
        <FlashcardsDataGrid />
    </Paper>
  );
}
