import { CssBaseline, ThemeProvider } from "@mui/material";
import { Routes, Route } from "react-router-dom";
import { themeSettings } from "./theme";
import { useState } from "react";
import Navbar from "./scenes/Navbar";
import Dashboard from "./scenes/Dashboard";
import FileUpload from "./scenes/FileUpload";

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
            <Route path="/fileupload" element={<FileUpload />} />
          </Routes>
        </main>
      </div>
    </ThemeProvider>
  );
}

export default App;
