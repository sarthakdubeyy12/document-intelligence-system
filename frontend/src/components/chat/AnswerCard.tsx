"use client";

import React from "react";

interface AnswerCardProps {
  answer?: string;
  isLoading?: boolean;
  error?: string | null;
}

export default function AnswerCard({ answer, isLoading = false, error }: AnswerCardProps) {
  const content = isLoading ? "Generating answer..." : answer || "Upload a document and ask a question to begin.";

  return (
    <div className="bg-gradient-to-br from-white to-blue-50 dark:from-gray-800 dark:to-gray-900 rounded-3xl p-8 md:p-10 border border-blue-100 dark:border-gray-700 shadow-xl">
      <div className="flex items-center justify-between gap-3 mb-6">
        <h3 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
          Answer
        </h3>
        <span className="px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 text-xs font-semibold uppercase tracking-[0.24em]">
          Primary Output
        </span>
      </div>

      <div className="prose prose-sm md:prose-base dark:prose-invert max-w-none">
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-base md:text-lg">
          {content}
        </p>
      </div>

      {error ? (
        <div className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl">
          <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
        </div>
      ) : !answer && !isLoading ? (
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl">
          <p className="text-sm text-blue-700 dark:text-blue-300">
            Once connected, your answer will appear here with grounded context from the uploaded document.
          </p>
        </div>
      ) : null}
    </div>
  );
}
