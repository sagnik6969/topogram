import { useState, useRef, useEffect } from "react";
import { Sidebar } from "@excalidraw/excalidraw";
import { Send, Bot } from "lucide-react";
import "./AiSidebar.css";

interface Message {
    id: string;
    text: string;
    sender: "user" | "ai";
    timestamp: number;
}

export const AiSidebar = ({ isDocked, setIsDocked }: { isDocked: boolean, setIsDocked: (isDocked: boolean) => void }) => {
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
    }, [messages]);

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

    return (
        <Sidebar name="ai-agent" className="ai-sidebar" docked={isDocked} onDock={(docked) => setIsDocked(docked)}>
            <div className="ai-sidebar-container">
                <div className="ai-sidebar-header">
                    <h3>AI Assistant</h3>
                </div>

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
                    <button className="ai-chat-send-btn" onClick={handleSend} disabled={!input.trim()}>
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </Sidebar>
    );
};
