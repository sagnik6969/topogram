import { useState, useRef, useEffect } from "react";
import { Sidebar } from "@excalidraw/excalidraw";
import { Send, Bot, LogOut } from "lucide-react";
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signInWithPopup,
    GoogleAuthProvider,
    signOut,
    onAuthStateChanged,
    type User
} from "firebase/auth";
import { auth } from "./firebase";
import "./AiSidebar.css";

interface Message {
    id: string;
    text: string;
    sender: "user" | "ai";
    timestamp: number;
}

export const AiSidebar = ({ isDocked, setIsDocked }: { isDocked: boolean, setIsDocked: (isDocked: boolean) => void }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoginMode, setIsLoginMode] = useState(true);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [authError, setAuthError] = useState<string | null>(null);

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

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
            setUser(currentUser);
        });
        return () => unsubscribe();
    }, []);

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

    const handleAuth = async (e: React.FormEvent) => {
        e.preventDefault();
        setAuthError(null);
        try {
            if (isLoginMode) {
                await signInWithEmailAndPassword(auth, email, password);
            } else {
                await createUserWithEmailAndPassword(auth, email, password);
            }
        } catch (error: any) {
            setAuthError(error.message);
        }
    };

    const handleGoogleLogin = async () => {
        setAuthError(null);
        const provider = new GoogleAuthProvider();
        try {
            await signInWithPopup(auth, provider);
        } catch (error: any) {
            console.error("Error signing in with Google: ", error);
            setAuthError(error.message);
        }
    };

    const handleLogout = async () => {
        try {
            await signOut(auth);
            setMessages([{ // Reset messages on logout if desired
                id: "1",
                text: "Hello! I'm your AI assistant. How can I help you with your diagram today?",
                sender: "ai",
                timestamp: Date.now(),
            }]);
        } catch (error) {
            console.error("Error signing out: ", error);
        }
    };

    return (
        <Sidebar name="ai-agent" className="ai-sidebar" docked={isDocked} onDock={(docked) => setIsDocked(docked)}>
            <div className="ai-sidebar-container">
                <Sidebar.Header>
                    <div className="ai-sidebar-header">
                        <h3>AI Assistant</h3>
                        {user && (
                            <div className="ai-header-actions">
                                <button className="ai-logout-btn" onClick={handleLogout} title="Sign out">
                                    <LogOut size={16} />
                                </button>
                            </div>
                        )}
                    </div>
                </Sidebar.Header>

                {!user ? (
                    <div className="ai-auth-container">
                        <div className="ai-auth-header">
                            <h2>{isLoginMode ? "Welcome Back" : "Create Account"}</h2>
                            <p>{isLoginMode ? "Sign in to access AI features" : "Sign up to start using AI"}</p>
                        </div>

                        {authError && <div className="ai-auth-error">{authError}</div>}

                        <form className="ai-auth-form" onSubmit={handleAuth}>
                            <input
                                type="email"
                                className="ai-auth-input"
                                placeholder="Email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                            <input
                                type="password"
                                className="ai-auth-input"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            <button type="submit" className="ai-auth-btn">
                                {isLoginMode ? "Sign In" : "Sign Up"}
                            </button>
                        </form>

                        <div className="ai-auth-divider">or continue with</div>

                        <button className="ai-auth-google-btn" onClick={handleGoogleLogin}>
                            <svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
                                <path d="M17.64 9.20455C17.64 8.56636 17.5827 7.95273 17.4764 7.36364H9V10.845H13.8436C13.635 11.97 13.0009 12.9232 12.0477 13.5614V15.8195H14.9564C16.6582 14.2527 17.64 11.9455 17.64 9.20455Z" fill="#4285F4" />
                                <path d="M9 18C11.43 18 13.4673 17.1941 14.9564 15.8195L12.0477 13.5614C11.2418 14.1014 10.2109 14.4205 9 14.4205C6.65591 14.4205 4.67182 12.8373 3.96409 10.71H0.957275V13.0418C2.43818 15.9832 5.48182 18 9 18Z" fill="#34A853" />
                                <path d="M3.96409 10.71C3.78409 10.17 3.68182 9.59318 3.68182 9C3.68182 8.40682 3.78409 7.83 3.96409 7.29V4.95818H0.957275C0.347727 6.17318 0 7.54773 0 9C0 10.4523 0.347727 11.8268 0.957275 13.0418L3.96409 10.71Z" fill="#FBBC05" />
                                <path d="M9 3.57955C10.3214 3.57955 11.5077 4.03364 12.4405 4.92545L15.0218 2.34409C13.4632 0.891818 11.4259 0 9 0C5.48182 0 2.43818 2.01682 0.957275 4.95818L3.96409 7.29C4.67182 5.16273 6.65591 3.57955 9 3.57955Z" fill="#EA4335" />
                            </svg>
                            Google
                        </button>

                        <div className="ai-auth-toggle">
                            {isLoginMode ? "Don't have an account? " : "Already have an account? "}
                            <span onClick={() => setIsLoginMode(!isLoginMode)}>
                                {isLoginMode ? "Sign up" : "Sign in"}
                            </span>
                        </div>
                    </div>
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
                            <button className="ai-chat-send-btn" onClick={handleSend} disabled={!input.trim()}>
                                <Send size={18} />
                            </button>
                        </div>
                    </>
                )}
            </div>
        </Sidebar>
    );
};
