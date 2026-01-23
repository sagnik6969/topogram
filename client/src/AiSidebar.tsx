import { useState, useRef, useEffect } from "react";
import { Sidebar } from "@excalidraw/excalidraw";
import { Send, Bot, LogOut } from "lucide-react";
import { signOut } from "firebase/auth";
import { auth } from "./firebase";
import "./AiSidebar.css";
import apiClient from "./api/axiosClient";
import { Auth, useAuth } from "./Auth";

interface Message {
  id: string;
  text: string;
  sender: "user" | "ai";
  timestamp: number;
}

export const AiSidebar = ({
  isDocked,
  setIsDocked,
}: {
  isDocked: boolean;
  setIsDocked: (isDocked: boolean) => void;
}) => {
  const { user } = useAuth();

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Hello! I'm your AI assistant. How can I help you with your diagram today?",
      sender: "ai",
      timestamp: Date.now(),
    },
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, user]); // Scroll when messages change or user logs in (view changes)

  const handleSend = () => {
    if (!input.trim()) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: "user",
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    apiClient.post("/ai/message", {});

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: "I received your message! This is a mock response.",
        sender: "ai",
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, aiResponse]);
    }, 1000);
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      setMessages([
        {
          // Reset messages on logout if desired
          id: "1",
          text: "Hello! I'm your AI assistant. How can I help you with your diagram today?",
          sender: "ai",
          timestamp: Date.now(),
        },
      ]);
    } catch (error) {
      console.error("Error signing out: ", error);
    }
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
            <h3>AI Assistant</h3>
            {user && (
              <div className="ai-header-actions">
                <button
                  className="ai-logout-btn"
                  onClick={handleLogout}
                  title="Sign out"
                >
                  <LogOut size={16} />
                </button>
              </div>
            )}
          </div>
        </Sidebar.Header>

        {!user ? (
          <Auth />
        ) : (
          <>
            <div className="ai-chat-messages">
              {messages.map((msg) => (
                <div key={msg.id} className={`ai-chat-message ${msg.sender}`}>
                  {msg.sender === "ai" && (
                    <div className="ai-message-sender-label">
                      <Bot size={14} /> <span>AI Agent</span>
                    </div>
                  )}
                  {msg.text}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            <div className="ai-chat-input-area">
              <input
                type="text"
                className="ai-chat-input"
                placeholder="Type a message..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
              />
              <button
                className="ai-chat-send-btn"
                onClick={handleSend}
                disabled={!input.trim()}
              >
                <Send size={18} />
              </button>
            </div>
          </>
        )}
      </div>
    </Sidebar>
  );
};
