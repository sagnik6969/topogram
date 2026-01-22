import { useState } from "react";
import { Excalidraw, Sidebar } from "@excalidraw/excalidraw";
import "@excalidraw/excalidraw/index.css";
import "./App.css";
import { IconsSidebar } from "./IconsSidebar";
import { Brain, Cloud } from "lucide-react";

function App() {
  const [excalidrawAPI, setExcalidrawAPI] = useState<any>(null);

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
        <IconsSidebar excalidrawAPI={excalidrawAPI} />
      </Excalidraw>
    </div>
  );
}

export default App;
