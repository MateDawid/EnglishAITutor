import type { GridColDef } from "@mui/x-data-grid";
import { SINGLE_SELECT_FILTER_OPERATORS, STRING_FILTER_OPERATORS } from "./FlashcardsDataGrid.filtering";
import { EasyChip, MediumChip, HardChip, StyledChip } from "../SingleFlashcardModal/styles";
import { FlashcardRating } from "../../constants";

const WORD_COLUMN: GridColDef = {
  field: 'word',
  type: 'string',
  headerName: 'Word',
  headerAlign: 'left',
  align: 'left',
  flex: 2,
  filterable: true,
  sortable: true,
  filterOperators: STRING_FILTER_OPERATORS,
  renderCell: (params) => {
    const partOfSpeech = params.row.part_of_speech;
    return (
      <>
        {params.value} <StyledChip label={partOfSpeech} size="small" />
      </>
    );
  }
}

const RATING_COLUMN: GridColDef = {
  field: 'user_rating',
  type: 'singleSelect',
  headerName: 'Your Rating',
  headerAlign: 'right',
  align: 'right',
  flex: 1,
  filterable: true,
  sortable: false,
  filterOperators: SINGLE_SELECT_FILTER_OPERATORS,
  valueOptions: [
  { value: FlashcardRating.NOT_RATED, label: '✖️ Not rated' },
  { value: FlashcardRating.EASY, label: '🟢 Easy' },
  { value: FlashcardRating.MEDIUM, label: '🟡 Medium' },
  { value: FlashcardRating.HARD, label: '🔴 Hard' },
],
  renderCell: (params) => {
    switch (params.value) {
      case FlashcardRating.EASY:
        return <EasyChip label="Easy" size="small"/>;
      case FlashcardRating.MEDIUM:
        return <MediumChip label="Medium" size="small" />;
      case FlashcardRating.HARD:
        return <HardChip label="Hard" size="small" />;
      default:
        return null;
    }
  }
}

export const COLUMNS: GridColDef[] = [WORD_COLUMN, RATING_COLUMN];
