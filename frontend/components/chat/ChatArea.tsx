"use client";

import { useEffect, useRef } from "react";
import { MessageSquare } from "lucide-react";
import { ChatMessage, StreamingMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import type { ChatMessage as ChatMessageType } from "@/types";

interface ChatAreaProps {
  messages: ChatMessageType[];
  streamingContent: string | null;
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

export function ChatArea({
  messages,
  streamingContent,
  onSendMessage,
  isLoading,
}: ChatAreaProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, streamingContent]);

  return (
    <div className="flex-1 flex flex-col h-full bg-white dark:bg-gray-800">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 && !streamingContent ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8">
            <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center mb-4">
              <MessageSquare className="w-8 h-8 text-primary-600 dark:text-primary-400" />
            </div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              Welcome to SmartAsset
            </h2>
            <p className="text-gray-600 dark:text-gray-400 max-w-md mb-6">
              Your AI-powered financial advisor. Ask me about budgeting, Canadian taxes,
              TFSA, RRSP contributions, and more!
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-lg">
              {[
                "What are the 2024 TFSA contribution limits?",
                "Help me create a monthly budget",
                "Explain RRSP vs TFSA differences",
                "How do I file taxes in Canada?",
              ].map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => onSendMessage(suggestion)}
                  className="p-3 text-sm text-left bg-gray-100 dark:bg-gray-700
                           hover:bg-gray-200 dark:hover:bg-gray-600
                           rounded-lg transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="divide-y dark:divide-gray-700">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {streamingContent && <StreamingMessage content={streamingContent} />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <ChatInput onSend={onSendMessage} disabled={isLoading} />
    </div>
  );
}
