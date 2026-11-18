
-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Store document chunks and their embeddings
CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,

    content TEXT NOT NULL,

    embedding VECTOR(768) NOT NULL,

    source TEXT NOT NULL,

    page INTEGER,

    section TEXT,

    chunk_index INTEGER NOT NULL,

    strategy TEXT NOT NULL,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE (source, strategy, chunk_index)
);
