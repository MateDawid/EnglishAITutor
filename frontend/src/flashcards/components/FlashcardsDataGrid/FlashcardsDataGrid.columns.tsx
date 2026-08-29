import type { GridColDef } from "@mui/x-data-grid";
import { SINGLE_SELECT_FILTER_OPERATORS, STRING_FILTER_OPERATORS } from "./FlashcardsDataGrid.filtering";
import { EasyChip, MediumChip, HardChip, StyledChip } from "../SingleFlashcardModal/styles";
import { EASY_RATING_VALUE, HARD_RATING_VALUE, MEDIUM_RATING_VALUE } from "../../constants";

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
  headerAlign: 'right',
  align: 'right',
  flex: 1,
  filterable: true,
  sortable: true,
  filterOperators: SINGLE_SELECT_FILTER_OPERATORS,
  valueOptions: [
  { value: EASY_RATING_VALUE, label: 'Easy' },
  { value: MEDIUM_RATING_VALUE, label: 'Medium' },
  { value: HARD_RATING_VALUE, label: 'Hard' },
],
  renderCell: (params) => {
    switch (params.value) {
      case EASY_RATING_VALUE:
        return <EasyChip label="Easy" size="small"/>;
      case MEDIUM_RATING_VALUE:
        return <MediumChip label="Medium" size="small" />;
      case HARD_RATING_VALUE:
        return <HardChip label="Hard" size="small" />;
      default:
        return null;
    }
  }
}

export const COLUMNS: GridColDef[] = [WORD_COLUMN, RATING_COLUMN];
