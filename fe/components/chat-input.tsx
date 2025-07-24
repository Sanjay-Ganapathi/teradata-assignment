import { FormEvent, ChangeEvent } from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Send } from "lucide-react";

interface ChatInputProps {
    input: string;
    isLoading: boolean;
    handleInputChange: (e: ChangeEvent<HTMLInputElement>) => void;
    handleSubmit: (e: FormEvent) => void;
}

export function ChatInput({ input, isLoading, handleInputChange, handleSubmit }: ChatInputProps) {
    return (
        <div className="p-4 border-t bg-background">
            <form onSubmit={handleSubmit} className="flex space-x-4">
                <Input
                    value={input}
                    onChange={handleInputChange}
                    placeholder="Ask a question about your documents..."
                    disabled={isLoading}
                />
                <Button type="submit" disabled={isLoading}>
                    <Send className="h-4 w-4" />
                </Button>
            </form>
        </div>
    );
}