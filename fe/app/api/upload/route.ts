
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
    try {

        const formData = await req.formData();


        const response = await fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData,

        });


        const data = await response.json();


        if (!response.ok) {

            return NextResponse.json({ detail: data.detail || "Upload failed on backend" }, { status: response.status });
        }


        return NextResponse.json(data);

    } catch (error: any) {

        return NextResponse.json({ detail: error.message }, { status: 500 });
    }
}