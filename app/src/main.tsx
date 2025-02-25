import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {BrowserRouter, Route, Routes} from "react-router-dom";
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import './index.css'
import App from './App.tsx'
import HomePage from "./Pages/HomePage";
import {ThemeProvider} from "@mui/material";
import theme from "./theme";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <ThemeProvider theme={theme}>
        <BrowserRouter>
            <Routes>
                <Route element={<App />}>
                    <Route index element={<HomePage />} />
                    <Route/>
                </Route>
            </Routes>
        </BrowserRouter>
    </ThemeProvider>
  </StrictMode>
)
