import React from "react";
import { MantineProvider } from "@mantine/core";
import ChatbotUI from "./components/ChatBotUI";
import backgroundImage from "./assets/IEP_background.jpg";

function App() {
  const appStyle = {
    backgroundImage: `url(${backgroundImage})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    height: "100vh",
    width: "100vw",
    margin: 0,
    padding: 0,
  };
  return (
    <MantineProvider withGlobalStyles withNormalizeCSS>
      <div className="App" style={appStyle}>
        <ChatbotUI />
      </div>
    </MantineProvider>
  );
}

export default App;
