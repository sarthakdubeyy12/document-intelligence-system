export interface UploadFailedDocument {
  filename: string;
  error: string;
}

export interface UploadApiResponse {
  ingested: string[];
  failed: UploadFailedDocument[];
  chunk_count: number;
  stored_count: number;
}

export interface Citation {
  chunk_id?: string;
  filename: string;
  page_number?: number;
  pageNumber?: number;
  snippet: string;
}

export interface ChatApiResponse {
  answer: string;
  citations: Citation[];
}

export interface UploadSummary {
  documentsIngested: number;
  chunksCreated: number;
  vectorsStored: number;
}
