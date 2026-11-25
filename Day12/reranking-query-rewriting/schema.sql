
-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Store document chunks and their embeddings
CREATE TABLE IF NOT EXISTS document_chunks (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    metadata JSONB
);

ALTER TABLE document_chunks
ADD COLUMN search_vector TSVECTOR
GENERATED ALWAYS AS (
    to_tsvector('english', COALESCE(content, ''))
) STORED;

CREATE INDEX document_chunks_search_idx
ON document_chunks
USING GIN(search_vector);
