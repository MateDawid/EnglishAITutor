import { useEffect, useState } from 'react';

import FlashcardFront from './FlashcardFront';
import FlashcardBack from './FlashcardBack';
import { StyledModal, StyledPaper } from './styles';
import type { Flashcard } from '../../types';

export type SingleFlashcardModalProps = {
    flashcard: Flashcard | null;
    open: boolean;
    setOpen: (open: boolean) => void;
};

/**
 * SingleFlashcardModal component for displaying a single flashcard in a modal.
 * @param {object} props
 * @param {Flashcard | null} props.flashcard - The flashcard data to be displayed in the modal.
 * @param {boolean} props.open - Flag indicating if modal is opened.
 * @param {function} props.setOpen - Setter for open flag.
 */
const SingleFlashcardModal = ({
    flashcard,
    open,
    setOpen,
}: SingleFlashcardModalProps) => {
    const [cardReversed, setCardReversed] = useState(false);

    /**
     * Effect hook to handle modal open/close and card reversed state.
     */
    useEffect(() => {
        if (flashcard === null) {
            setOpen(false);
        }
        if (!open) {
            setCardReversed(false);
        }
    }, [open, flashcard]);

    return (
        <StyledModal
            open={open}
            onClose={() => {
                setOpen(false);
                setCardReversed(false);
            }}
        >
            <StyledPaper reversed={cardReversed}>
                {flashcard && (
                    <>
                        <FlashcardFront flashcard={flashcard} setCardReversed={setCardReversed} />
                        <FlashcardBack flashcard={flashcard} setOpen={setOpen} />
                    </>
                )}
            </StyledPaper>
        </StyledModal>
    );
};

export default SingleFlashcardModal;
