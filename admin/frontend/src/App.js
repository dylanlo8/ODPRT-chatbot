import Dashboard from "./scenes/Dashboard";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { themeSettings } from "./theme";

function App() {
  const theme = themeSettings();

  return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          <main className="content">
            <Dashboard />
          </main>
        </div>
      </ThemeProvider>
  );
}

export default App;
