"use client";

import React from "react";

export default function ChatSection() {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 border border-gray-200 dark:border-gray-700 shadow-lg">
      <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        Ask a Question
      </h3>

      <div className="space-y-4">
        <textarea
          placeholder="Ask anything about your documents... (e.g., 'What are the key findings?', 'Summarize the introduction', 'Find information about pricing')"
          className="w-full px-6 py-4 rounded-xl bg-gray-50 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          rows={4}
        />

        <button className="w-full sm:w-auto px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl">
          Ask Question
        </button>
      </div>

      <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">
        💡 Tip: Be specific in your questions to get more accurate results. You can ask about summaries, specific details, comparisons, and more.
      </p>
    </div>
  );
}
