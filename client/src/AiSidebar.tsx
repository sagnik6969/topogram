import { useState } from "react";
import { Sidebar } from "@excalidraw/excalidraw";
import {
  LogOut,
  Wand2,
  Copy,
} from "lucide-react";
import { signOut } from "firebase/auth";
import { auth } from "./firebase";
import "./AiSidebar.css";
import apiClient from "./api/axiosClient";
import { Auth, useAuth } from "./Auth";

interface PromptHistoryItem {
  id: string;
  prompt: string;
  timestamp: number;
}

export const AiSidebar = ({
  excalidrawAPI,
  isDocked,
  setIsDocked,
}: {
  excalidrawAPI: any;
  isDocked: boolean;
  setIsDocked: (isDocked: boolean) => void;
}) => {
  const { user } = useAuth();
  const [input, setInput] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [history, setHistory] = useState<PromptHistoryItem[]>([]);

  // We can keep track of session ID if needed, but for "Prompt History" view, we simply list local usages.
  const [chatId, setChatId] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!input.trim()) return;
    setIsGenerating(true);

    const newHistoryItem: PromptHistoryItem = {
      id: Date.now().toString(),
      prompt: input,
      timestamp: Date.now(),
    };

    // Add to history
    setHistory((prev) => [newHistoryItem, ...prev]);

    try {
      const response = await apiClient.post("/main_backend_service/v1/chat/", {
        user_message: input,
        thread_id: chatId,
      });

      // Store chat ID if it's the first message
      if (!chatId && response.data.thread_id) {
        setChatId(response.data.thread_id);
      }

      if (response.data.files) {
        excalidrawAPI.addFiles(response.data.files);
      }
      excalidrawAPI.updateScene(response.data);
      setInput("");
    } catch (error) {
      excalidrawAPI.setToast({
        message: "Error generating diagram. Please try again after refreshing the page.",
        closable: true,
        duration: 10000,

      })
      console.error("Error generating diagram:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      setHistory([]);
      setInput("");
      setChatId(null);
    } catch (error) {
      console.error("Error signing out: ", error);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <Sidebar
      name="ai-agent"
      className="ai-sidebar"
      docked={isDocked}
      onDock={(docked) => setIsDocked(docked)}
    >
      <div className="ai-sidebar-container">
        <Sidebar.Header>
          <div className="ai-sidebar-header">
            <h3>Diagram Copilot</h3>
            {user && (
              <button
                className="ai-logout-btn"
                onClick={handleLogout}
                title="Sign out"
              >
                <LogOut size={16} />
              </button>
            )}
          </div>
        </Sidebar.Header>

        {!user ? (
          <Auth />
        ) : (
          <div className="ai-content-wrapper">
            <div className="ai-prompt-section">
              <div className="ai-section-label">
                <span>Diagram Generation Prompt</span>
                <span className="ai-label-sub">Required</span>
              </div>

              <div className="ai-input-card">
                <textarea
                  className="ai-prompt-textarea"
                  placeholder="Create a detailed aws architecture diagram for a hr ticketing system with user authentication, database, and notification services."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      handleGenerate();
                    }
                  }}
                />
              </div>

              <div className="ai-generate-actions">
                <button
                  className="ai-generate-btn"
                  onClick={handleGenerate}
                  disabled={isGenerating || !input.trim()}
                >
                  {isGenerating ? (
                    <>
                      <Wand2 className="animate-spin" size={16} /> Generating...
                    </>
                  ) : (
                    <>
                      <Wand2 size={16} /> Generate
                    </>
                  )}
                </button>
              </div>
            </div>

            {history.length > 0 && (
              <div className="ai-history-section">
                <h4 className="ai-history-title">Prompt History</h4>
                <div className="ai-history-list">
                  {history.map((item) => (
                    <div key={item.id} className="ai-history-item">
                      <div className="ai-history-header">
                        <p className="ai-history-text">{item.prompt}</p>
                        <button
                          className="ai-copy-btn"
                          onClick={() => copyToClipboard(item.prompt)}
                          title="Copy prompt"
                        >
                          <Copy size={14} />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </Sidebar>
  );
};
