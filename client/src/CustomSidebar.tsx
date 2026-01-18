import { useState, useMemo } from "react";
import { Sidebar } from "@excalidraw/excalidraw";

interface IconItem {
  path: string;
  url: string;
  name: string;
}

export const CustomSidebar = ({ excalidrawAPI }: { excalidrawAPI: any }) => {
  const [searchTerm, setSearchTerm] = useState("");

  // Load icons eagerly as URLs using Vite's glob import
  const iconsGlob = import.meta.glob(
    "./assets/aws-icons/**/*.{svg,png,jpg,jpeg}",
    {
      eager: true,
      import: "default",
    },
  );

  const icons: IconItem[] = useMemo(() => {
    return Object.entries(iconsGlob).map(([path, url]) => {
      // Extract a readable name from the filename
      const filename = path.split("/").pop() || "icon";
      // Remove extensions and cleanup prefixes
      let name = filename
        .replace(/\.(svg|png|jpg|jpeg)$/, "")
        .replace(/^Arch_/, "")
        .replace(/_64$/, "")
        .replace(/_48$/, "")
        .replace(/_32$/, "")
        .replace(/_16$/, "");
      
      // Replace separators with spaces
      name = name.replace(/[_-]/g, " ");
      
      return {
        path,
        url: url as string,
        name,
      };
    });
  }, []);

  const filteredIcons = useMemo(() => {
    if (!searchTerm) return icons;
    const lower = searchTerm.toLowerCase();
    return icons.filter((i) => i.name.toLowerCase().includes(lower));
  }, [icons, searchTerm]);

  const addToScene = async (icon: IconItem) => {
    if (!excalidrawAPI) return;

    try {
      const response = await fetch(icon.url);
      const blob = await response.blob();
      
      const reader = new FileReader();
      reader.readAsDataURL(blob);
      reader.onloadend = () => {
        const base64data = reader.result as string;
        
        const fileId = Math.random().toString(36).substring(2, 15);
        const imageId = Math.random().toString(36).substring(2, 15);
        const textId = Math.random().toString(36).substring(2, 15);
        const groupId = Math.random().toString(36).substring(2, 15);

        const appState = excalidrawAPI.getAppState();
        const { scrollX, scrollY, width, height, zoom } = appState;
        
        // Center the new image in the viewport
        const sceneX = (width / 2) / zoom.value - scrollX - 32;
        const sceneY = (height / 2) / zoom.value - scrollY - 32;

        const file = {
            id: fileId,
            mimeType: blob.type || "image/svg+xml",
            dataURL: base64data,
            created: Date.now(),
            lastRetrieved: Date.now()
        };

        const imageElement = {
            id: imageId,
            type: "image",
            x: sceneX,
            y: sceneY,
            width: 64, 
            height: 64,
            angle: 0,
            strokeColor: "transparent",
            backgroundColor: "transparent",
            fillStyle: "hachure",
            strokeWidth: 1,
            strokeStyle: "solid",
            roughness: 1,
            opacity: 100,
            groupIds: [groupId],
            frameId: null,
            roundness: null,
            seed: Math.floor(Math.random() * 100000),
            version: 1,
            versionNonce: 0,
            isDeleted: false,
            boundElements: null,
            updated: Date.now(),
            link: null,
            locked: false,
            fileId: fileId,
            scale: [1, 1],
            status: "saved",
        };

        // Helper to wrap text
        const wrapText = (str: string, maxChars: number) => {
          const words = str.split(" ");
          const lines: string[] = [];
          let currentLine = words[0];

          for (let i = 1; i < words.length; i++) {
            if (currentLine.length + 1 + words[i].length <= maxChars) {
              currentLine += " " + words[i];
            } else {
              lines.push(currentLine);
              currentLine = words[i];
            }
          }
          lines.push(currentLine);
          return lines.join("\n");
        };

        const wrappedText = wrapText(icon.name, 15); // Wrap at ~15 chars
        
        // Font settings for Nunito (Sans-serif = 2)
        const fontSize = 16;
        const fontFamily = 2; // Normal (Helvetica/Sans-serif -> mapped to Nunito in CSS)
        const lineHeight = 1.25;
        
        // Measure text with wrapped lines
        const lines = wrappedText.split("\n");
        const maxLineLength = Math.max(...lines.map(l => l.length));
        const numberOfLines = lines.length;
        
        const charWidth = fontSize * 0.55; // Approximation for Sans-serif
        const textWidth = Math.max(maxLineLength * charWidth, 20);
        const textHeight = fontSize * lineHeight * numberOfLines;
        
        const textX = sceneX + 32 - (textWidth / 2); // Center text below image

        const textElement = {
            id: textId,
            type: "text",
            x: textX,
            y: sceneY + 70,
            width: textWidth,
            height: textHeight,
            angle: 0,
            strokeColor: "#1e1e1e",
            backgroundColor: "transparent",
            fillStyle: "hachure",
            strokeWidth: 1,
            strokeStyle: "solid",
            roughness: 1,
            opacity: 100,
            groupIds: [groupId],
            frameId: null,
            roundness: null,
            seed: Math.floor(Math.random() * 100000),
            version: 1,
            versionNonce: 0,
            isDeleted: false,
            boundElements: null,
            updated: Date.now(),
            link: null,
            locked: false,
            text: wrappedText,
            fontSize: fontSize,
            fontFamily: fontFamily,
            textAlign: "center",
            verticalAlign: "top",
            baseline: 14,
            containerId: null,
            originalText: wrappedText,
            lineHeight: lineHeight,
            status: "saved",
        };

        excalidrawAPI.addFiles([file]);
        excalidrawAPI.updateScene({
            elements: [...excalidrawAPI.getSceneElements(), imageElement, textElement],
        });
      };
    } catch (err) {
      console.error("Error adding icon to scene:", err);
    }
  };

  return (
    <Sidebar name="aws-icons" className="custom-sidebar" docked={true}>
      <Sidebar.Header>
         <h3 style={{ margin: 0, padding: "0.5rem" }}>AWS Icons</h3>
      </Sidebar.Header>
      <div style={{ display: "flex", flexDirection: "column", padding: "0.5rem", height: "100%", boxSizing: "border-box" }}>
        <input
          type="text"
          placeholder="Search icons..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            padding: "8px",
            marginBottom: "10px",
            borderRadius: "4px",
            border: "1px solid #ccc",
            width: "100%",
            boxSizing: "border-box"
          }}
        />
        <div style={{ flex: 1, overflowY: "auto", display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "10px", alignContent: "start", paddingBottom: "20px" }}>
          {filteredIcons.map((icon) => (
            <div
              key={icon.path}
              title={icon.name}
              onClick={() => addToScene(icon)}
              style={{
                cursor: "pointer",
                border: "1px solid #eee",
                borderRadius: "4px",
                padding: "8px 4px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "flex-start",
                gap: "5px",
                backgroundColor: "#fff",
                height: "auto",
                minHeight: "100px"
              }}
            >
              <div style={{ width: "48px", height: "48px", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <img 
                  src={icon.url} 
                  alt={icon.name} 
                  style={{ maxWidth: "100%", maxHeight: "100%", objectFit: "contain" }} 
                />
              </div>
              <span style={{ fontSize: "10px", textAlign: "center", wordBreak: "break-word", lineHeight: "1.2" }}>{icon.name}</span>
            </div>
          ))}
          {filteredIcons.length === 0 && (
            <div
              style={{
                gridColumn: "1/-1",
                textAlign: "center",
                color: "#666",
                marginTop: "20px",
              }}
            >
              No icons found
            </div>
          )}
        </div>
      </div>
    </Sidebar>
  );
};
