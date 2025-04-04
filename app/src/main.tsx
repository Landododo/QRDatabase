import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {BrowserRouter, Navigate, Outlet, Route, Routes} from "react-router-dom";
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import './index.css'
import App from './App.tsx'
import HomePage from "./Pages/HomePage";
import {ThemeProvider} from "@mui/material";
import theme from "./theme";
import { CodeViewer } from './Pages/IndividualCodeViewer.tsx';
import { ChipViewer } from './Components/ChipViewer.tsx';
import { PayloadContext } from './data/payload.ts';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <ThemeProvider theme={theme}>
        <PayloadContext.Provider value={{codesX:125, codesY: 100, spacingX: 0.2, spacingY: 0.2, layer: []}}>
          <BrowserRouter>
              <Routes>
                  <Route element={<App />}>
                      <Route index element={<HomePage />} />
                      <Route path=":projectId" element={<Outlet />}>
                          <Route index element={<ChipViewer />} />
                          <Route path="upload" element={<h1>project level upload</h1>} />
                          <Route path="manage" element={<h1>project level manage</h1>} />
                          <Route path=":codeid" element ={<CodeViewer/>}>
                        </Route>
                      </Route>
                  </Route>
              </Routes>
          </BrowserRouter>
        </PayloadContext.Provider>
    </ThemeProvider>
  </StrictMode>
)
