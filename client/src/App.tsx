import { useState } from "react";
import { Excalidraw, Sidebar } from "@excalidraw/excalidraw";
import "@excalidraw/excalidraw/index.css";

import "./App.css";
import { CustomSidebar } from "./CustomSidebar";

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
          <Sidebar.Trigger name="aws-icons">AWS Icons</Sidebar.Trigger>
        )}
      >
        <CustomSidebar excalidrawAPI={excalidrawAPI} />
      </Excalidraw>
    </div>
  );
}

export default App;
