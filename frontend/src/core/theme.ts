import { createTheme } from '@mui/material/styles';

declare module '@mui/material/styles' {
  interface Palette {
    rating: {
      easyLight: string;
      easyDark: string;
      mediumLight: string;
      mediumDark: string;
      hardLight: string;
      hardDark: string;
    };
  }

  interface PaletteOptions {
    rating?: {
      easyLight: string;
      easyDark: string;
      mediumLight: string;
      mediumDark: string;
      hardLight: string;
      hardDark: string;
    };
  }
}

export const theme = createTheme({
  palette: {
    primary: {
      main: "#34204c",
      light: "#baa8bd",
      dark: "#000000",
      contrastText: "#ffffff",
      ratingEasyLight: "#2E7D32",
      ratingEasyDark: "#1B5E20",
      ratingMediumLight: "#F57C00",
      ratingMediumDark: "#EF6C00",
      ratingHardLight: "#C62828",
      ratingHardDark: "#B71C1C",
    },
  }
});