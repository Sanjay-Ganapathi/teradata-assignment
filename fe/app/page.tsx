
"use client";

import { ChatMessages } from "@/components/chat-message";
import { ChatInput } from "@/components/chat-input";
import { Header } from "@/components/header"
import { useChat } from "@/hooks/use-chat";

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat();

  return (
    <div className="flex flex-col h-screen bg-background">
      <Header />
      <main className="flex-1 flex flex-col pt-16">
        <ChatMessages messages={messages} isLoading={isLoading} />
        <ChatInput
          input={input}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
        />
      </main>
    </div>
  );
}