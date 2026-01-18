import { useState } from "react";
import MermaidRenderer from "./MermaidRenderer";
import "./App.css";

function App() {
  const [code, setCode] = useState<string>(`%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
graph TD
  A[Client] --> B[Load Balancer]
  B --> C[Server01]
  B --> D[Server02]
`);

  return (
    <div style={{ display: "flex", height: "100vh", width: "100vw", overflow: "hidden" }}>
      {/* Editor Section */}
      <div style={{ width: "50%", padding: "1rem", borderRight: "1px solid #ccc", display: "flex", flexDirection: "column" }}>
        <h2>Mermaid Editor</h2>
        <textarea
          style={{
            flex: 1,
            width: "100%",
            padding: "1rem",
            fontSize: "16px",
            fontFamily: "monospace",
            resize: "none",
            border: "1px solid #ccc",
            borderRadius: "4px",
          }}
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />
      </div>

      {/* Preview Section */}
      <div style={{ width: "50%", padding: "1rem", backgroundColor: "#f9f9f9", overflow: "auto" }}>
        <h2>Preview</h2>
        <div style={{ border: "1px solid #ccc", borderRadius: "4px", padding: "1rem", backgroundColor: "white", minHeight: "300px" }}>
          <MermaidRenderer chart={code} />
        </div>
      </div>
    </div>
  );
}

export default App;
