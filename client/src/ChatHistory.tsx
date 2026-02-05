import React, { useEffect, useState, useRef } from 'react';
import apiClient from "./api/axiosClient";
import "./ChatHistory.css";
import { Clock, MessageSquare, ChevronRight, Loader2 } from 'lucide-react';

interface Checkpoint {
    structured_response: {
        nodes: any[];
        edges: any[];
    };
    messages: {
        content: string;
        type: string;
        [key: string]: any;
    }[];
}

export interface ChatSession {
    id: string;
    updated_at: string;
    checkpoint: Checkpoint;
    created_at: string;
    user_id: string;
}

interface ChatHistoryProps {
    onSelectChat: (chat: ChatSession) => void;
    isOpen: boolean;
    onClose: () => void;
}

export const ChatHistory: React.FC<ChatHistoryProps> = ({ onSelectChat, isOpen, onClose }) => {
    const [chats, setChats] = useState<ChatSession[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [hasMore, setHasMore] = useState(true);
    const [offset, setOffset] = useState(0);
    const limit = 20;

    const dropdownRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                onClose();
            }
        }

        if (isOpen) {
            document.addEventListener("mousedown", handleClickOutside);
        }
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [isOpen, onClose]);

    useEffect(() => {
        if (isOpen && chats.length === 0) {
            fetchChats();
        }
    }, [isOpen]);

    const fetchChats = async () => {
        if (loading || (!hasMore && offset !== 0)) return;
        setLoading(true);
        setError(null);
        try {
            const response = await apiClient.get(`/v1/chat/?limit=${limit}&offset=${offset}`);
            const newChats = response.data;
            if (newChats.length < limit) {
                setHasMore(false);
            }
            setChats(prev => [...prev, ...newChats]);
            setOffset(prev => prev + limit);
        } catch (err) {
            setError("Failed to load chat history");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="chat-history-dropdown" ref={dropdownRef}>
            <div className="chat-history-header">
                <h3><Clock size={16} /> History</h3>
            </div>
            <div className="chat-history-list">
                {chats.map(chat => {
                    const firstUserMessage = chat.checkpoint?.messages?.find(m => m.type === 'human')?.content || "New Chat";
                    const date = new Date(chat.updated_at).toLocaleDateString();
                    return (
                        <div key={chat.id} className="chat-history-item" onClick={() => onSelectChat(chat)}>
                            <div className="chat-history-icon">
                                <MessageSquare size={16} />
                            </div>
                            <div className="chat-history-info">
                                <div className="chat-history-title" title={firstUserMessage}>{firstUserMessage}</div>
                                <div className="chat-history-date">{date}</div>
                            </div>
                            <ChevronRight size={14} className="chat-history-arrow" />
                        </div>
                    )
                })}
                {loading && <div className="chat-history-loader"><Loader2 className="animate-spin" size={20} /></div>}
                {!loading && hasMore && (
                    <button className="chat-history-load-more" onClick={fetchChats}>Load more</button>
                )}
                {!loading && chats.length === 0 && <div className="chat-history-empty">No history found</div>}
                {error && <div className="chat-history-error">{error}</div>}
            </div>
        </div>
    );
};
