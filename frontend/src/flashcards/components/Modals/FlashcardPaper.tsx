import { useState } from 'react';

import FlashcardFront from './FlashcardFront';
import FlashcardBack from './FlashcardBack';
import type { Flashcard } from '../../types';
import type { JSX } from 'react';
import { StyledPaper } from '../styles';

export type FlashcardPaperProps = {
    flashcard: Flashcard;
    cardReversed: boolean;
    setCardReversed: (reversed: boolean) => void;
    handleClose: (ratingChanged?: boolean) => void;
    setRefreshTimestamp: (timestamp: number | null) => void;
};

/**
 * FlashcardPaper component for displaying a single flashcard in a modal.
 * @param {object} props
 * @param {Flashcard} props.flashcard - The flashcard data to be displayed in the modal.
 * @param {function} props.setRefreshTimestamp - Setter for refresh timestamp.
 * @param {function} props.handleClose - Handler for closing the modal.
 */
const FlashcardPaper = ({ flashcard, cardReversed, setCardReversed, setRefreshTimestamp, handleClose }: FlashcardPaperProps): JSX.Element => {

    return (
        <StyledPaper reversed={cardReversed} rating={flashcard.rating}>
            {flashcard && (
                <>
                    <FlashcardFront flashcard={flashcard} setCardReversed={setCardReversed} />
                    <FlashcardBack flashcard={flashcard} handleClose={handleClose} setRefreshTimestamp={setRefreshTimestamp} />
                </>
            )}
        </StyledPaper>
    );
};

export default FlashcardPaper;
