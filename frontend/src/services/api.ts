import { request } from "@/lib/axios";
import type { ChatApiResponse, UploadApiResponse } from "@/types/api";

export async function uploadDocuments(files: File[]) {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  return request<UploadApiResponse>("/api/upload", {
    method: "POST",
    body: formData,
  });
}

export async function askQuestion(question: string) {
  return request<ChatApiResponse>("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });
}
