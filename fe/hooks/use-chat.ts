
import { useState, FormEvent, ChangeEvent } from 'react';
import { toast } from "sonner"
import cuid from 'cuid';
export interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
}

export function useChat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);


    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInput(e.target.value);
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage: Message = { id: cuid(), role: "user", content: input };
        const newMessages = [...messages, userMessage];
        setMessages(newMessages);
        setInput("");
        setIsLoading(true);
        const assistantMessageId = cuid();
        const assistantMessagePlaceholder: Message = { id: assistantMessageId, role: "assistant", content: "" };
        setMessages(prev => [...prev, assistantMessagePlaceholder]);

        try {
            const response = await fetch("/api/chat/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ messages: newMessages.map(({ id, ...rest }) => rest) }),

            });
            if (!response.ok || !response.body) {
                throw new Error(`An error occurred: ${response.statusText}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();




            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                if (chunk) setIsLoading(false);


                setMessages(prev =>
                    prev.map(msg =>
                        msg.id === assistantMessageId
                            ? { ...msg, content: msg.content + chunk }
                            : msg
                    )
                );
            }

        } catch (error: any) {
            toast("Error", {

                description: error.message,

            });
            setMessages(prev => prev.filter(msg => msg.id !== assistantMessageId));
        } finally {
            setIsLoading(false);
        }
    };

    return { messages, input, isLoading, handleInputChange, handleSubmit };
}