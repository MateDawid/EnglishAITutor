import { useState } from 'react';

import FlashcardFront from './FlashcardFront';
import FlashcardBack from './FlashcardBack';
import type { Flashcard } from '../../types';
import type { JSX } from "@emotion/react/jsx-dev-runtime";
import { StyledModal, StyledPaper } from './styles';

export type SingleFlashcardModalProps = {
    flashcard: Flashcard | null;
    open: boolean;
    setOpen: (open: boolean) => void;
    setRefreshTimestamp: (timestamp: number | null) => void;
};

/**
 * SingleFlashcardModal component for displaying a single flashcard in a modal.
 * @param {object} props
 * @param {Flashcard | null} props.flashcard - The flashcard data to be displayed in the modal.
 * @param {boolean} props.open - Flag indicating if modal is opened.
 * @param {function} props.setOpen - Setter for open flag.
 * @param {function} props.setRefreshTimestamp - Setter for refresh timestamp.
 */
const SingleFlashcardModal = ({
    flashcard,
    open,
    setOpen,
    setRefreshTimestamp,
}: SingleFlashcardModalProps): JSX.Element => {
    const [cardReversed, setCardReversed] = useState(false);

    const handleClose = () => {
        setOpen(false);
        setCardReversed(false);
    }

    return (
        <StyledModal
            open={open && flashcard !== null}
            onClose={handleClose}
        >
            <StyledPaper reversed={cardReversed}>
                {flashcard && (
                    <>
                        <FlashcardFront flashcard={flashcard} setCardReversed={setCardReversed} />
                        <FlashcardBack flashcard={flashcard} handleClose={handleClose} setRefreshTimestamp={setRefreshTimestamp} />
                    </>
                )}
            </StyledPaper>
        </StyledModal>
    );
};

export default SingleFlashcardModal;
