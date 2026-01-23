import { useState } from "react";
import { Excalidraw, MainMenu, Sidebar } from "@excalidraw/excalidraw";
import "@excalidraw/excalidraw/index.css";
import "./App.css";
import { IconsSidebar } from "./IconsSidebar";
import { AiSidebar } from "./AiSidebar";
import { Brain, Github, Linkedin } from "lucide-react";
import { app } from "./firebase";
function App() {
  const [excalidrawAPI, setExcalidrawAPI] = useState<any>(null);
  const [isIconsSidebarDocked, setIsIconsSidebarDocked] = useState<boolean>(false);
  const [isAiSidebarDocked, setIsAiSidebarDocked] = useState<boolean>(false);

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        width: "100%",
        overflow: "hidden",
      }}
    >
      <Excalidraw
        excalidrawAPI={(api) => setExcalidrawAPI(api)}
        renderTopRightUI={() => (
          <>
            <Sidebar.Trigger icon={<Brain />} name="ai-agent">
              Ask AI
            </Sidebar.Trigger>
            <Sidebar.Trigger name="icons-sidebar">AWS Icons</Sidebar.Trigger>
          </>
        )}
      >
        <MainMenu>
          <MainMenu.Group>
            <MainMenu.DefaultItems.LoadScene />
            <MainMenu.DefaultItems.Export />
            <MainMenu.DefaultItems.SaveAsImage />
            <MainMenu.DefaultItems.ClearCanvas />
            <MainMenu.DefaultItems.ToggleTheme />
          </MainMenu.Group>
          <MainMenu.Group title="Socials">
            <MainMenu.ItemLink icon={<Github />} href="https://github.com/sagnik6969" target="_blank">
              GitHub
            </MainMenu.ItemLink>
            <MainMenu.ItemLink icon={<Linkedin />} href="https://www.linkedin.com/in/sagnik-jana-3452771ba/" target="_blank">
              Linkedin
            </MainMenu.ItemLink>
          </MainMenu.Group>
          <MainMenu.DefaultItems.ChangeCanvasBackground />
        </MainMenu>
        <IconsSidebar
          excalidrawAPI={excalidrawAPI} isDocked={isIconsSidebarDocked} setIsDocked={setIsIconsSidebarDocked} />
        <AiSidebar isDocked={isAiSidebarDocked} setIsDocked={setIsAiSidebarDocked} />
      </Excalidraw>
    </div>
  );
}

export default App;
