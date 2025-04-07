import { CssBaseline, ThemeProvider } from "@mui/material";
import { Routes, Route } from "react-router-dom";
import { themeSettings } from "./theme";
import { useState } from "react";
import Navbar from "./scenes/Navbar";
import Dashboard from "./scenes/Dashboard";
import FileUpload from "./scenes/FileUpload";
import './App.css';

function App() {
  const theme = themeSettings();
  const [isCollapsed, setIsCollapsed] = useState(true);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
        <Navbar isCollapsed={isCollapsed} setIsCollapsed={setIsCollapsed} />

        {/* OVERLAY */}
        {!isCollapsed && (
          <div
            className="overlay"
            onClick={() => setIsCollapsed(true)}
          />
        )}

        {/* MAIN CONTENT */}
        <main
          className="content"
          style={{
            marginLeft: "90px",
            transition: "opacity 0.3s ease",
            opacity: isCollapsed ? 1 : 0.5,
            position: "relative", 
            zIndex: 0,
          }}
        >
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
