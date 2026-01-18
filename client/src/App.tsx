import { useState } from "react";
import { Excalidraw } from "@excalidraw/excalidraw";
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
          <button
            style={{
              border: "1px solid #ced4da",
              borderRadius: "4px",
              padding: "0.5rem 1rem",
              cursor: "pointer",
              height: "2.5rem",
              fontWeight: 600,
              fontSize: "0.875rem",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              backgroundColor: "#404040",
              color: "white",
            }}
            onClick={() => {
              excalidrawAPI?.updateScene({
                appState: { openSidebar: { name: "aws-icons" } },
              });
            }}
          >
            AWS Icons
          </button>
        )}
      >
        <CustomSidebar excalidrawAPI={excalidrawAPI} />
      </Excalidraw>
    </div>
  );
}

export default App;
