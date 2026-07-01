"use client";

import { useCallback, useState } from "react";

import { uploadDocuments } from "@/services/api";
import type { UploadSummary } from "@/types/api";

type UploadStatus = "idle" | "uploading" | "processing" | "embedding" | "completed";

const initialSummary: UploadSummary = {
  documentsIngested: 0,
  chunksCreated: 0,
  vectorsStored: 0,
};

export function useUpload() {
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>("idle");
  const [isUploading, setIsUploading] = useState(false);
  const [uploadSummary, setUploadSummary] = useState<UploadSummary>(initialSummary);
  const [error, setError] = useState<string | null>(null);

  const uploadFiles = useCallback(async (files: File[]) => {
    if (!files.length) {
      setError("Please select at least one PDF file.");
      return;
    }

    if (files.length > 50) {
      setError("You can upload between 1 and 50 PDF files.");
      return;
    }

    const invalidFiles = files.filter(
      (file) => !file.name.toLowerCase().endsWith(".pdf"),
    );

    if (invalidFiles.length) {
      setError("Please upload only PDF files.");
      return;
    }

    setError(null);
    setIsUploading(true);
    setUploadStatus("uploading");

    try {
      const response = await uploadDocuments(files);
      setUploadSummary({
        documentsIngested: response.ingested.length,
        chunksCreated: response.chunk_count,
        vectorsStored: response.stored_count,
      });
      setUploadStatus("completed");
    } catch (err) {
      setUploadStatus("idle");
      setError(err instanceof Error ? err.message : "Upload failed.");
    } finally {
      setIsUploading(false);
    }
  }, []);

  return {
    uploadFiles,
    uploadStatus,
    isUploading,
    uploadSummary,
    error,
    clearError: () => setError(null),
  };
}
