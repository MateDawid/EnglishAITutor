import type { GridColDef } from "@mui/x-data-grid";
import { SINGLE_SELECT_FILTER_OPERATORS, STRING_FILTER_OPERATORS } from "./FlashcardsDataGrid.filtering";

const WORD_COLUMN: GridColDef =  {
    field: 'word',
    type: 'string',
    headerName: 'Word',
    headerAlign: 'left',
    align: 'left',
    flex: 1,
    filterable: true,
    sortable: true,
    filterOperators: STRING_FILTER_OPERATORS,
  }

const PART_OF_SPEECH_COLUMN: GridColDef =  {
    field: 'part_of_speech',
    type: 'singleSelect',
    headerName: 'Part of speech',
    headerAlign: 'left',
    align: 'left',
    flex: 1,
    filterable: true,
    sortable: false,
    filterOperators: SINGLE_SELECT_FILTER_OPERATORS,
    valueOptions: [
      { value: 'noun', label: 'Noun' },
      { value: 'verb', label: 'Verb' },
      { value: 'adjective', label: 'Adjective' },
      { value: 'adverb', label: 'Adverb' },
      { value: 'pronoun', label: 'Pronoun' },
      { value: 'preposition', label: 'Preposition' },
      { value: 'conjunction', label: 'Conjunction' },
      { value: 'interjection', label: 'Interjection' },
    ],
  }

const MEANING_COLUMN: GridColDef =  {
    field: 'meaning',
    type: 'string',
    headerName: 'Meaning',
    headerAlign: 'left',
    align: 'left',
    flex: 3,
    filterable: true,
    sortable: false,
    filterOperators: STRING_FILTER_OPERATORS,
  }

export const ALL_COLUMNS: GridColDef[] = [WORD_COLUMN, PART_OF_SPEECH_COLUMN, MEANING_COLUMN];
export const MINIMUM_COLUMNS: GridColDef[] = [WORD_COLUMN, MEANING_COLUMN];
