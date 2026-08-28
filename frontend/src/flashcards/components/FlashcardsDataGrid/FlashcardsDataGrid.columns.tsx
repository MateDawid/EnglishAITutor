import type { GridColDef } from "@mui/x-data-grid";
import { SINGLE_SELECT_FILTER_OPERATORS, STRING_FILTER_OPERATORS } from "./FlashcardsDataGrid.filtering";
import { EasyChip, MediumChip, HardChip, StyledChip } from "../SingleFlashcardModal/styles";

const EASY_VALUE = 1;
const MEDIUM_VALUE = 2;
const HARD_VALUE = 3;

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
  field: 'rating',
  type: 'singleSelect',
  headerName: 'Your Rating',
  headerAlign: 'left',
  align: 'left',
  flex: 1,
  filterable: true,
  sortable: true,
  filterOperators: SINGLE_SELECT_FILTER_OPERATORS,
  valueOptions: [
  { value: EASY_VALUE, label: 'Easy' },
  { value: MEDIUM_VALUE, label: 'Medium' },
  { value: HARD_VALUE, label: 'Hard' },
],
  renderCell: (params) => {
    switch (params.value) {
      case EASY_VALUE:
        return <EasyChip label="Easy" size="small"/>;
      case MEDIUM_VALUE:
        return <MediumChip label="Medium" size="small" />;
      case HARD_VALUE:
        return <HardChip label="Hard" size="small" />;
      default:
        return null;
    }
  }
}

export const COLUMNS: GridColDef[] = [WORD_COLUMN, RATING_COLUMN];
