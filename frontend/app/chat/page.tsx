"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { ChatSidebar } from "@/components/chat/ChatSidebar";
import { ChatArea } from "@/components/chat/ChatArea";
import { useAuth } from "@/hooks/useAuth";
import { api } from "@/lib/api";
import type { ChatSession, ChatMessage } from "@/types";

export default function ChatPage() {
  const router = useRouter();
  const { user, isLoading: authLoading, isAuthenticated, logout } = useAuth();

  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [streamingContent, setStreamingContent] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/auth/login");
    }
  }, [authLoading, isAuthenticated, router]);

  // Load sessions
  useEffect(() => {
    if (isAuthenticated) {
      loadSessions();
    }
  }, [isAuthenticated]);

  const loadSessions = async () => {
    try {
      const sessionsData = await api.getSessions();
      setSessions(sessionsData);
    } catch (error) {
      console.error("Failed to load sessions:", error);
    }
  };

  const loadSession = useCallback(async (sessionId: number) => {
    try {
      const session = await api.getSession(sessionId);
      setMessages(session.messages);
      setCurrentSessionId(sessionId);
    } catch (error) {
      console.error("Failed to load session:", error);
    }
  }, []);

  const handleNewChat = () => {
    setCurrentSessionId(null);
    setMessages([]);
    setStreamingContent(null);
  };

  const handleSelectSession = (sessionId: number) => {
    loadSession(sessionId);
  };

  const handleDeleteSession = async (sessionId: number) => {
    try {
      await api.deleteSession(sessionId);
      setSessions((prev) => prev.filter((s) => s.id !== sessionId));
      if (currentSessionId === sessionId) {
        handleNewChat();
      }
    } catch (error) {
      console.error("Failed to delete session:", error);
    }
  };

  const handleSendMessage = async (content: string) => {
    setIsLoading(true);
    setStreamingContent("");

    // Optimistically add user message
    const tempUserMessage: ChatMessage = {
      id: Date.now(),
      session_id: currentSessionId || 0,
      role: "user",
      content,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMessage]);

    try {
      const response = await api.sendMessage(content, currentSessionId || undefined);

      // Update session ID if this was a new chat
      if (!currentSessionId) {
        setCurrentSessionId(response.session_id);
        await loadSessions();
      }

      // Replace temp message with real ones
      setMessages((prev) => {
        const withoutTemp = prev.filter((m) => m.id !== tempUserMessage.id);
        return [...withoutTemp, response.user_message, response.assistant_message];
      });
      setStreamingContent(null);
    } catch (error) {
      console.error("Failed to send message:", error);
      setStreamingContent(null);
      // Remove optimistic message on error
      setMessages((prev) => prev.filter((m) => m.id !== tempUserMessage.id));
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    router.push("/auth/login");
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex h-screen">
      <ChatSidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={handleSelectSession}
        onNewChat={handleNewChat}
        onDeleteSession={handleDeleteSession}
        onLogout={handleLogout}
        userName={user?.full_name || user?.email}
      />
      <ChatArea
        messages={messages}
        streamingContent={streamingContent}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
}
