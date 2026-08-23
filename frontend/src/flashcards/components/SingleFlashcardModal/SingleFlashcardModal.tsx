import { useEffect, useState } from 'react';

import FlashcardFront from './FlashcardFront';
import FlashcardBack from './FlashcardBack';
import type { Flashcard } from './types';
import { StyledModal, StyledPaper } from './styles';

export type SingleFlashcardModalProps = {
    flashcard: Flashcard;
    open: boolean;
    setOpen: (open: boolean) => void;
};

/**
 * FormModal component for displaying add/edit form.
 * @param {object} props
 * @param {object} props.flashcard - The flashcard data to be displayed in the modal.
 * @param {boolean} props.open - Flag indicating if form is opened.
 * @param {function} props.setOpen - Setter for open flag.
 */
const SingleFlashcardModal = ({
    flashcard,
    open,
    setOpen,
}: SingleFlashcardModalProps) => {
    const [cardReversed, setCardReversed] = useState(false);

    useEffect(() => {
        if (!open) {
            setCardReversed(false);
        }
    }, [open]);

    return (
        <StyledModal
            open={open}
            onClose={() => {
                setOpen(false);
                setCardReversed(false);
            }}
        >
            <StyledPaper reversed={cardReversed}>
                <FlashcardFront flashcard={flashcard} setCardReversed={setCardReversed} />
                <FlashcardBack flashcard={flashcard} setOpen={setOpen} />
            </StyledPaper>
        </StyledModal>
    );
};

export default SingleFlashcardModal;
