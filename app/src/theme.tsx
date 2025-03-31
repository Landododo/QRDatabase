import { createTheme } from '@mui/material/styles';
import { red } from '@mui/material/colors';

// A custom theme for this app
const theme = createTheme({
    cssVariables: true,
    palette: {
        primary: {
            main: '#2560d5',
        },
        secondary: {
            main: '#c0c0c0',
        },
        error: {
            main: red.A400,
        },
        info: {
            main: "#d8d8d8"
        }
    },
});

export default theme;