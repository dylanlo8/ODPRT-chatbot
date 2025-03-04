import Dashboard from "./scenes/Dashboard";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { Routes, Route } from "react-router-dom";
import { themeSettings } from "././theme";
import { useState } from "react";
import Navbar from "./scenes/Navbar";

function App() {
  const theme = themeSettings();
  const [isNavbar] = useState(true);

  return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
        <Navbar isNavbar={isNavbar} />
          <main className="content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
            </Routes>
          </main>
        </div>
      </ThemeProvider>
  );
}

export default App;
