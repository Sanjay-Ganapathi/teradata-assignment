
import { useEffect, useRef } from "react";
import { Message } from "@/hooks/use-chat";
import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";

interface ChatMessagesProps {
    messages: Message[];
    isLoading: boolean;
}

export function ChatMessages({ messages, isLoading }: ChatMessagesProps) {
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg, index) => (
                <div
                    key={msg.id}
                    className={cn(
                        "flex items-end",
                        msg.role === "user" ? "justify-end" : "justify-start"
                    )}
                >
                    {msg.content && <div
                        className={cn(
                            "max-w-xl px-4 py-2 rounded-lg whitespace-pre-wrap",
                            msg.role === "user"
                                ? "bg-primary text-primary-foreground"
                                : "bg-muted"
                        )}
                    >
                        <p className="text-sm">{msg.content}</p>
                    </div>}
                </div>
            ))}
            {isLoading && (
                <div className="flex items-end justify-start">
                    <div className="max-w-xl px-4 py-2 rounded-lg bg-muted flex items-center space-x-2">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span className="text-sm">Thinking...</span>
                    </div>
                </div>
            )}
            <div ref={scrollRef} />
        </div>
    );
}