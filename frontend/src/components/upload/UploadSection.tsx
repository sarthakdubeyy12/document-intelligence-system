"use client";

import React from "react";

interface UploadSectionProps {
  uploadStatus?: "idle" | "uploading" | "processing" | "embedding" | "completed";
  isUploading?: boolean;
}

const statusSteps = [
  { key: "uploading", label: "Uploading..." },
  { key: "processing", label: "Processing..." },
  { key: "embedding", label: "Embedding..." },
  { key: "completed", label: "Completed ✓" },
] as const;

export default function UploadSection({
  uploadStatus = "idle",
  isUploading = false,
}: UploadSectionProps) {
  const activeStep = statusSteps.findIndex((step) => step.key === uploadStatus);
  const isDisabled = isUploading || uploadStatus === "uploading" || uploadStatus === "processing" || uploadStatus === "embedding";

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 border border-gray-200 dark:border-gray-700 shadow-lg">
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        Upload Documents
      </h3>
      <p className="text-gray-600 dark:text-gray-400 mb-6">
        Upload 1–50 PDF documents for analysis.
      </p>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <button
          type="button"
          disabled={isDisabled}
          className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-blue-500 to-purple-600 px-5 py-2.5 text-sm font-semibold text-white transition-all duration-300 hover:from-blue-600 hover:to-purple-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isUploading ? "Uploading…" : "Upload Files"}
        </button>

        <div className="text-sm text-gray-500 dark:text-gray-400">
          {uploadStatus === "idle" ? "Ready to begin" : statusSteps[Math.max(activeStep, 0)]?.label}
        </div>
      </div>

      <div className="mt-6 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-12 text-center hover:border-blue-500 dark:hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/10 transition-all duration-300 cursor-pointer group">
        <div className="text-5xl mb-4 group-hover:scale-110 transition-transform duration-300">
          📄
        </div>
        <p className="text-gray-700 dark:text-gray-300 font-semibold mb-2">
          Drag and drop your files here
        </p>
        <p className="text-gray-500 dark:text-gray-400 text-sm mb-4">
          or click to browse from your computer
        </p>
        <p className="text-xs text-gray-500 dark:text-gray-500">
          Supported formats: PDF, DOCX, TXT (Max 50MB)
        </p>
      </div>

      <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">0</p>
          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
            Documents Ingested
          </p>
        </div>
        <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p className="text-2xl font-bold text-green-600 dark:text-green-400">0</p>
          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
            Chunks Created
          </p>
        </div>
        <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">0</p>
          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
            Vectors Stored
          </p>
        </div>
      </div>
    </div>
  );
}
