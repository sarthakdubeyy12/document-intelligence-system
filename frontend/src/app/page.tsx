"use client";

import WavyBackground from "@/components/background/WavyBackground";
import UploadSection from "@/components/upload/UploadSection";
import ChatSection from "@/components/chat/ChatSection";
import AnswerCard from "@/components/chat/AnswerCard";
import CitationList from "@/components/chat/CitationList";
import Footer from "@/components/common/Footer";
import { useChat } from "@/hooks/useChat";
import { useUpload } from "@/hooks/useUpload";

export default function Home() {
  const {
    uploadFiles,
    uploadStatus,
    isUploading,
    uploadSummary,
    error: uploadError,
  } = useUpload();

  const {
    question,
    setQuestion,
    answer,
    citations,
    isAsking,
    error: chatError,
    askQuestion,
  } = useChat();

  return (
    <div className="w-full">
      {/* Home Section - Full Screen with Wavy Background */}
      <div className="w-full h-screen relative overflow-hidden">
        <WavyBackground className="w-full h-full flex flex-col items-center justify-center">
          <div className="relative z-10 px-4 text-center max-w-3xl">
            <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold text-white">
              Document Intelligence System
            </h1>
            <p className="mt-6 text-base sm:text-lg md:text-xl text-white/90 leading-relaxed">
              Upload one or more PDF documents, ask questions in natural language, and receive grounded answers with citations.
            </p>
          </div>
        </WavyBackground>
      </div>

      {/* Upload Section */}
      <section id="upload" className="w-full min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col items-center justify-center px-4 py-20 relative z-20">
        <div className="max-w-4xl w-full">
          <div className="text-center mb-8">
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-500 dark:text-blue-400 mb-3">
              Step 1
            </p>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white">
              Upload Documents
            </h2>
          </div>
          <p className="text-lg text-gray-600 dark:text-gray-400 text-center mb-12">
            Start by uploading your documents. Then ask questions and get instant answers with citations.
          </p>
          <UploadSection
            uploadStatus={uploadStatus}
            isUploading={isUploading}
            uploadSummary={uploadSummary}
            error={uploadError}
            onUpload={uploadFiles}
          />
        </div>
      </section>

      {/* Ask Questions Section */}
      <section id="ask" className="w-full min-h-screen bg-white dark:bg-gray-800 flex flex-col items-center justify-center px-4 py-20 relative z-20">
        <div className="max-w-4xl w-full">
          <div className="text-center mb-8">
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-500 dark:text-blue-400 mb-3">
              Step 2
            </p>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white">
              Ask Questions
            </h2>
          </div>

          {/* Main Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column - Chat Section */}
            <div className="lg:col-span-1">
              <ChatSection
                question={question}
                onQuestionChange={setQuestion}
                onAsk={askQuestion}
                isLoading={isAsking}
                error={chatError}
              />
            </div>

            {/* Right Column - Answer and Citations */}
            <div className="lg:col-span-2 space-y-8">
              <AnswerCard answer={answer} isLoading={isAsking} error={chatError} />
              <CitationList citations={citations} />
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
