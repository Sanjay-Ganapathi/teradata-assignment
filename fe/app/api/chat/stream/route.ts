import { NextRequest } from "next/server";

export const runtime = "edge";

export async function POST(req: NextRequest) {
    try {
        const { messages } = await req.json();


        const response = await fetch("http://localhost:8000/chat/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ messages }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Backend error: ${response.status} ${errorText}`);
        }

        return new Response(response.body, {
            headers: { "Content-Type": "text/plain" },
        });

    } catch (error: any) {
        return new Response(error.message, { status: 500 });
    }
}