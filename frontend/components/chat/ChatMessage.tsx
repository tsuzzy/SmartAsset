"use client";

import { User, Bot } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ChatMessage as ChatMessageType } from "@/types";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "flex gap-4 p-4",
        isUser ? "bg-white dark:bg-gray-800" : "bg-gray-50 dark:bg-gray-900"
      )}
    >
      <div
        className={cn(
          "w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0",
          isUser
            ? "bg-primary-600 text-white"
            : "bg-emerald-600 text-white"
        )}
      >
        {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
      </div>
      <div className="flex-1 space-y-2">
        <p className="font-medium text-sm text-gray-500 dark:text-gray-400">
          {isUser ? "You" : "SmartAsset"}
        </p>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          {message.content.split("\n").map((line, index) => (
            <p key={index} className="mb-2 last:mb-0">
              {line}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
}

interface StreamingMessageProps {
  content: string;
}

export function StreamingMessage({ content }: StreamingMessageProps) {
  return (
    <div className="flex gap-4 p-4 bg-gray-50 dark:bg-gray-900">
      <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 bg-emerald-600 text-white">
        <Bot className="w-5 h-5" />
      </div>
      <div className="flex-1 space-y-2">
        <p className="font-medium text-sm text-gray-500 dark:text-gray-400">
          SmartAsset
        </p>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          {content.split("\n").map((line, index) => (
            <p key={index} className="mb-2 last:mb-0">
              {line}
            </p>
          ))}
          <span className="inline-block w-2 h-4 bg-gray-400 animate-pulse ml-1" />
        </div>
      </div>
    </div>
  );
}
