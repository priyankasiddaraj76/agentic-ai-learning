
-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Store document chunks and their embeddings
CREATE TABLE IF NOT EXISTS document_chunks (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    metadata JSONB
);
