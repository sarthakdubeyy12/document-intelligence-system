"use client";

import { useCallback, useState } from "react";

import { askQuestion } from "@/services/api";
import type { Citation } from "@/types/api";

export function useChat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | undefined>();
  const [citations, setCitations] = useState<Citation[]>([]);
  const [isAsking, setIsAsking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendQuestion = useCallback(async (value: string) => {
    const trimmed = value.trim();

    if (!trimmed) {
      setError("Please enter a question before submitting.");
      return;
    }

    setError(null);
    setIsAsking(true);

    try {
      const response = await askQuestion(trimmed);
      setAnswer(response.answer);
      setCitations(response.citations);
    } catch (err) {
      setAnswer(undefined);
      setCitations([]);
      setError(err instanceof Error ? err.message : "Unable to generate an answer.");
    } finally {
      setIsAsking(false);
    }
  }, []);

  return {
    question,
    setQuestion,
    answer,
    citations,
    isAsking,
    error,
    askQuestion: sendQuestion,
    clearError: () => setError(null),
  };
}
