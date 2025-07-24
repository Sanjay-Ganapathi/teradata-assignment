// fe/app/upload/page.tsx
"use client";

import { useState, ChangeEvent, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Header } from "@/components/header";
import { Loader2, UploadCloud } from "lucide-react";

export default function UploadPage() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isLoading, setIsLoading] = useState(false);


    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setSelectedFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            toast("No file selected", {

                description: "Please select a file to upload.",

            });
            return;
        }
        setIsLoading(true);

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {

            const response = await fetch("/api/upload", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Upload failed");
            }

            toast("Success!", {

                description: `"${selectedFile.name}" has been processed successfully.`,

            });

        } catch (error: any) {
            toast("Upload Error", {

                description: error.message,

            });
        } finally {
            setIsLoading(false);
            setSelectedFile(null);

            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }
        }
    };

    return (
        <div className="flex flex-col h-screen bg-background text-foreground">
            <Header />
            <main className="flex-1 flex items-center justify-center p-4">
                <Card className="w-full max-w-md">
                    <CardHeader>
                        <CardTitle className="flex items-center">
                            <UploadCloud className="mr-2 h-5 w-5" />
                            Upload Document
                        </CardTitle>
                        <CardDescription>
                            Upload a .txt or .pdf file to add it to your agents knowledge base.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid w-full items-center gap-4">
                            <div className="flex flex-col space-y-1.5">
                                <Label htmlFor="document">File</Label>
                                <Input
                                    id="document"
                                    type="file"
                                    ref={fileInputRef}
                                    onChange={handleFileChange}
                                    accept=".txt,.pdf"
                                />
                            </div>
                            <Button onClick={handleUpload} disabled={isLoading || !selectedFile} className="w-full">
                                {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : "Upload File"}
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </main>
        </div>
    );
}