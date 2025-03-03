import { createTheme } from "@mui/material/styles"; 

// colour design tokens 
export const tokens = () => ({ 
    main_background: "#F7F6F6",
    text: "#000000",
    white: "#FFFFFF",
    green: {
      100: "#e3f1dd",
      200: "#c7e4ba",
      300: "#aad698",
      400: "#8ec975",
      500: "#72bb53",
      600: "#5b9642",
      700: "#447032",
      800: "#2e4b21",
      900: "#172511"
    },
    red: {
      100: "#ffd7d3",
      200: "#ffafa7",
      300: "#ff887b",
      400: "#ff604f",
      500: "#ff3823",
      600: "#cc2d1c",
      700: "#992215",
      800: "#66160e",
      900: "#330b07"
    },
    gray: {
      100: "#f3f4f9",
      200: "#e7e8f3",
      300: "#dadded",
      400: "#ced1e7",
      500: "#c2c6e1",
      600: "#9b9eb4",
      700: "#747787",
      800: "#4e4f5a",
      900: "#27282d"
    },
    indigo: {
      100: "#d5dae9",
      200: "#abb5d3",
      300: "#8290bc",
      400: "#586ba6",
      500: "#2e4690",
      600: "#253873",
      700: "#1c2a56",
      800: "#121c3a",
      900: "#090e1d"
    }
})

export const themeSettings = () => {
  const colours = tokens();

  return createTheme({
    palette: {
      primary: {
        main: colours.indigo[500],
        light: colours.indigo[300],
        dark: colours.indigo[700],
      },
      secondary: {
        main: colours.gray[500],
        light: colours.gray[300],
        dark: colours.gray[700],
      },
      status: {
        increasing: colours.green[500],
        decreasing: colours.red[500],
      },
      background: {
        default: colours.main_background,
      },
      component: {
        default: colours.white, 
      },
      text: {
        primary: colours.text,
      },
    },
    typography: {
      fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
      fontSize: 12,
      h1: {
        fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
        fontSize: 40, 
      },
      h2: {
        fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
        fontSize: 32,
      },
      h3: {
        fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
        fontSize: 24,
      },
      h4: {
        fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
        fontSize: 20,
      },
      h5: {
        fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
        fontSize: 16,
      },
      h6: {
        fontFamily: ["Source Sans Pro", "sans-serif"].join(","),
        fontSize: 14,
      },
    },
  });
};