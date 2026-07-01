"use client";

import React from "react";

interface Citation {
  filename: string;
  pageNumber: number;
  snippet: string;
}

interface CitationListProps {
  citations?: Citation[];
}

const placeholderCitations: Citation[] = [
  {
    filename: "policy.pdf",
    pageNumber: 3,
    snippet: '"This policy states..."',
  },
  {
    filename: "policy.pdf",
    pageNumber: 7,
    snippet: '"The procedure applies to all approved teams."',
  },
  {
    filename: "policy.pdf",
    pageNumber: 11,
    snippet: '"Additional review is required for high-risk requests."',
  },
];

export default function CitationList({ citations }: CitationListProps) {
  const displayCitations = citations || placeholderCitations;

  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 border border-gray-200 dark:border-gray-700 shadow-lg">
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Citations
      </h3>

      {displayCitations.length > 0 ? (
        <div className="space-y-4">
          {displayCitations.map((citation, index) => (
            <div
              key={index}
              className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500 transition-colors duration-200"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-lg flex items-center justify-center">
                  <span className="text-white text-sm font-semibold">
                    {index + 1}
                  </span>
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 mb-2">
                    <h4 className="text-sm font-semibold text-gray-900 dark:text-white truncate">
                      {citation.filename}
                    </h4>
                    <span className="inline-block px-3 py-1 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-full text-xs font-medium whitespace-nowrap">
                      Page {citation.pageNumber}
                    </span>
                  </div>

                  <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                    "{citation.snippet}"
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg text-center">
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            Ask a question to see relevant sources from your documents.
          </p>
        </div>
      )}
    </div>
  );
}
