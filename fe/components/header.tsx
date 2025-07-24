
import Link from "next/link";
import { Button } from "./ui/button";

export function Header() {
    return (
        <header className="absolute top-0 left-0 right-0 p-4 bg-background/50 backdrop-blur-sm flex justify-between items-center border-b">
            <h1 className="text-xl font-bold">Agentic RAG</h1>
            <nav className="flex items-center space-x-4">
                <Button variant="ghost" asChild>
                    <Link href="/">Chat</Link>
                </Button>
                <Button variant="ghost" asChild>
                    <Link href="/upload">Upload</Link>
                </Button>
            </nav>
        </header>
    );
}