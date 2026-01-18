"use client";

import { useState } from "react";
import { MessageSquarePlus, Trash2, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { ChatSession } from "@/types";

interface ChatSidebarProps {
  sessions: ChatSession[];
  currentSessionId: number | null;
  onSelectSession: (sessionId: number) => void;
  onNewChat: () => void;
  onDeleteSession: (sessionId: number) => void;
  onLogout: () => void;
  userName?: string;
}

export function ChatSidebar({
  sessions,
  currentSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
  onLogout,
  userName,
}: ChatSidebarProps) {
  const [hoveredSession, setHoveredSession] = useState<number | null>(null);

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <h1 className="text-xl font-bold text-primary-400">SmartAsset</h1>
        <p className="text-xs text-gray-400 mt-1">AI Financial Advisor</p>
      </div>

      {/* New Chat Button */}
      <div className="p-3">
        <Button
          onClick={onNewChat}
          variant="secondary"
          className="w-full justify-start bg-gray-800 hover:bg-gray-700 text-white"
        >
          <MessageSquarePlus className="w-4 h-4 mr-2" />
          New Chat
        </Button>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto px-2">
        <div className="space-y-1">
          {sessions.map((session) => (
            <div
              key={session.id}
              className={cn(
                "group flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-colors",
                currentSessionId === session.id
                  ? "bg-gray-700"
                  : "hover:bg-gray-800"
              )}
              onClick={() => onSelectSession(session.id)}
              onMouseEnter={() => setHoveredSession(session.id)}
              onMouseLeave={() => setHoveredSession(null)}
            >
              <span className="text-sm truncate flex-1">{session.title}</span>
              {hoveredSession === session.id && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteSession(session.id);
                  }}
                  className="p-1 hover:bg-gray-600 rounded"
                >
                  <Trash2 className="w-4 h-4 text-gray-400 hover:text-red-400" />
                </button>
              )}
            </div>
          ))}
        </div>

        {sessions.length === 0 && (
          <p className="text-sm text-gray-500 text-center py-4">
            No conversations yet
          </p>
        )}
      </div>

      {/* User Section */}
      <div className="p-3 border-t border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium">
                {userName?.charAt(0).toUpperCase() || "U"}
              </span>
            </div>
            <span className="text-sm truncate max-w-[120px]">
              {userName || "User"}
            </span>
          </div>
          <button
            onClick={onLogout}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
            title="Logout"
          >
            <LogOut className="w-4 h-4 text-gray-400" />
          </button>
        </div>
      </div>
    </div>
  );
}
