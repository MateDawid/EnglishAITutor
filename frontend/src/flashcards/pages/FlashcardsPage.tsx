
import { Alert, Paper, Typography } from '@mui/material';
import FlashcardsDataGrid from '../components/FlashcardsDataGrid';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import { useState } from 'react';

/**
 * FlashcardsPage component to display list of Flashcards and manage flashcard-related actions.
 */
export default function FlashcardsPage() {
  document.title = 'Flashcards';
  const [showExactSearchAlert, setShowExactSearchAlert] = useState(true);

  return (
    <Paper
      elevation={24}
      sx={{
        padding: 2,
        margin: 2,
        border: '3px solid #1f1f1f',
        borderRadius: 0,
        boxShadow: '3px 3px 0 #1f1f1f',
      }}
    >
      <Typography
        variant="h4"
        component="h1"
        gutterBottom
        sx={{
          fontFamily: '"Arial Black", sans-serif !important',
          fontWeight: 'normal !important',
        }}
      >
        Flashcards
      </Typography>
      {showExactSearchAlert && (
        <Alert
          icon={<InfoOutlinedIcon />}
          severity="info"
          onClose={() => {setShowExactSearchAlert(false)}}
          sx={{
            padding: 2,
            margin: 1,
            border: '3px solid #1f1f1f',
            borderRadius: 0,
            boxShadow: '3px 3px 0 #1f1f1f',
          }}
        >
          Use parentheses in <strong>Word</strong> column filter to search for exact words or phrases. For example, searching for <strong>"end"</strong> will return <strong>end</strong> word, but will not return <strong>weekend</strong>.
        </Alert>
      )}
      <FlashcardsDataGrid />
    </Paper >
  );
}
