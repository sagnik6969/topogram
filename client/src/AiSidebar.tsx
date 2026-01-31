import { useState, useRef, useEffect } from "react";
import { Sidebar } from "@excalidraw/excalidraw";
import { Send, Bot, LogOut, History, Plus, Terminal } from "lucide-react";
import { signOut } from "firebase/auth";
import { auth } from "./firebase";
import "./AiSidebar.css";
import apiClient from "./api/axiosClient";
import { Auth, useAuth } from "./Auth";
import { ChatHistory, type ChatSession } from "./ChatHistory";

interface Message {
  id: string;
  text: string;
  sender: "user" | "ai" | "tool";
  name?: string;
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
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      text: "Hello! I'm your AI assistant. How can I help you with your diagram today?",
      sender: "ai",
      timestamp: Date.now(),
    },
  ]);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, user]); // Scroll when messages change or user logs in (view changes)

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: "user",
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    const response = await apiClient.post("/main_backend_service/v1/chat/", {
      user_message: input,
    });

    excalidrawAPI.addFiles(response.data.files);

    excalidrawAPI.updateScene(response.data);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: "Successfully generated the diagram!",
        sender: "ai",
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, aiResponse]);
    }, 1000);
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      startNewChat();
    } catch (error) {
      console.error("Error signing out: ", error);
    }
  };

  const startNewChat = () => {
    setMessages([
      {
        id: "1",
        text: "Hello! I'm your AI assistant. How can I help you with your diagram today?",
        sender: "ai",
        timestamp: Date.now(),
      },
    ]);
    setIsHistoryOpen(false);
  };

  const handleSelectChat = (chat: ChatSession) => {
    if (chat.checkpoint?.messages) {
      const loadedMessages: Message[] = chat.checkpoint.messages.map((m, idx) => ({
        id: m.id || `${chat.id}-${idx}`,
        text: m.content,
        sender: m.type === 'human' ? 'user' : (m.type === 'tool' ? 'tool' : 'ai'),
        name: m.name || (m.type === 'tool' ? 'Tool' : undefined),
        timestamp: Date.now(), // Timestamps are not preserved in this view of history
      }));
      setMessages(loadedMessages);
    }
    setIsHistoryOpen(false);
  };

  const formatMessageContent = (text: string) => {
    try {
      // Check if it looks like JSON/Array before parsing to avoid parsing simple numbers/bools if unwanted
      if ((text.trim().startsWith('{') || text.trim().startsWith('['))) {
        const parsed = JSON.parse(text);
        if (typeof parsed === 'object' && parsed !== null) {
          return <div className="ai-code-block">{JSON.stringify(parsed, null, 2)}</div>;
        }
      }
    } catch (e) {
      // Not JSON
    }
    return text;
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
            <div className="ai-header-actions">
              {user && (
                <>
                  <button
                    className="ai-logout-btn"
                    onClick={startNewChat}
                    title="New Chat"
                  >
                    <Plus size={16} />
                  </button>
                  <button
                    className="ai-logout-btn"
                    onClick={() => setIsHistoryOpen(!isHistoryOpen)}
                    title="Chat History"
                  >
                    <History size={16} />
                  </button>
                  <button
                    className="ai-logout-btn"
                    onClick={handleLogout}
                    title="Sign out"
                  >
                    <LogOut size={16} />
                  </button>
                </>
              )}
            </div>
          </div>
        </Sidebar.Header>

        <ChatHistory
          isOpen={isHistoryOpen}
          onClose={() => setIsHistoryOpen(false)}
          onSelectChat={handleSelectChat}
        />

        {!user ? (
          <Auth />
        ) : (
          <>
            <div className="ai-chat-messages">
              {messages.map((msg) => {
                // If message content is empty/blank, skip rendering
                if (!msg.text) return null;

                return (
                  <div key={msg.id} className={`ai-chat-message ${msg.sender}`}>
                    {msg.sender === "ai" && (
                      <div className="ai-message-sender-label">
                        <Bot size={14} /> <span>AI Agent</span>
                      </div>
                    )}
                    {msg.sender === "tool" && (
                      <div className="tool-name-label">
                        <Terminal size={14} /> <span>{msg.name || "Tool Output"}</span>
                      </div>
                    )}
                    {formatMessageContent(msg.text)}
                  </div>
                )
              })}
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
