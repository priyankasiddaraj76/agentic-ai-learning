# Day 10: Naive RAG

A command-line retrieval-augmented generation (RAG) example for asking
questions about computational biology lecture material. It retrieves similar
text chunks from PostgreSQL with pgvector, asks Gemini to answer using those
chunks, and validates that the answer's citations refer to retrieved chunks.

## How it works

1. The question is embedded with Gemini's `gemini-embedding-001` model as a
   `RETRIEVAL_QUERY` embedding.
2. PostgreSQL ranks rows in `document_chunks` by cosine distance (`<=>`) and
   returns the three nearest chunks.
3. The retrieved content and chunk IDs are added to a prompt for the Gemini
   answer model.
4. Gemini returns a JSON answer and citation IDs.
5. Pydantic validates the response, and the citation validator rejects IDs
   that were not among the retrieved chunks.

The embedding size is **768 dimensions**. Stored document embeddings and query
embeddings must use the same model and dimensions.

## Project layout

```text
naive-rag/
  data/                 # Chunk JSON inputs (not automatically ingested)
  src/
    config.py           # Model names and environment configuration
    embeddings.py       # Gemini query embeddings
    generator.py        # Gemini answer generation
    main.py             # Interactive command-line entry point
    prompt.py           # Context-grounded prompt
    retriever.py        # pgvector similarity search
    validators.py       # Response and citation validation
  requirements.txt
  schema.sql            # pgvector extension and document_chunks table
```

## Prerequisites

- Python 3.13 or Docker Desktop.
- A PostgreSQL database with the pgvector extension installed.
- A Gemini API key with access to the configured embedding and generation
  models.
- A populated `document_chunks` table containing content and 768-dimensional
  embeddings.

> **Important:** This project currently has no ingestion script. Local JSON
> chunks under `data/` are not included in this repository and are not loaded
> by `python -m src.main`. Create/load document rows and embeddings before
> running a search. If the table is empty, the app returns “No relevant
> information found.”

## Configure environment

Create a local `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=postgresql://appuser:your-password@localhost:5432/vectordb
```

Use the username, password, host, port, and database name for your PostgreSQL
instance. Keep `.env` private; it is excluded from Git.

## Initialize the database

The schema enables pgvector and creates `document_chunks` with a 768-dimensional
embedding column. From PowerShell, run this in the project directory, replacing
the container, user, and database names if yours differ:

```powershell
Get-Content .\schema.sql | docker exec -i day9-postgre psql -U appuser -d vectordb
```

The pipe is used because PowerShell does not support `< schema.sql` as input
redirection. `CREATE TABLE IF NOT EXISTS` does not migrate or change an existing
table. If reusing a database, verify its table has `id`, `content`, and
`embedding` columns and that its embeddings are 768-dimensional.

## Run

### Windows with Docker

If Windows Application Control blocks psycopg's native DLL, run the app in a
Linux Python container instead. Make sure PostgreSQL is running and its
container is named `day9-postgre` (or update the network target below).

From the project directory in PowerShell:

```powershell
docker run --rm -it `
  --network container:day9-postgre `
  --mount "type=bind,source=$($PWD.Path),target=/app" `
  -w /app `
  --env-file .env `
  python:3.13-slim `
  sh -c "pip install --no-cache-dir -r requirements.txt && python -m src.main"
```

The `-it` options keep the interactive question prompt connected. With
`--network container:day9-postgre`, the application container shares the
PostgreSQL container's network namespace; the database host in `DATABASE_URL`
can therefore be `localhost`.

### Local Python environment

If your Python environment is allowed to load psycopg's native driver:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.main
```

The application prompts for a question and prints the answer, citations, and
retrieved chunk IDs with similarity scores.

## Troubleshooting

- **`no pq wrapper available` or Application Control blocks a DLL:** use the
  Docker instructions rather than reinstalling psycopg repeatedly.
- **Database does not exist:** create the database or update `DATABASE_URL` to
  an existing database.
- **`different vector dimensions`:** ensure query embeddings and every stored
  embedding use 768 dimensions. Changing the query size does not resize vectors
  already stored in the database.
- **“No relevant information found”:** check that `document_chunks` contains
  rows with non-null embeddings. This app searches but does not ingest the
  chunk JSON files.
- **DNS, quota, or API errors:** check network access and the Gemini project's
  API quota; these are separate from PostgreSQL search.

## Dependencies

The project uses Google Gen AI (`google-genai`), Psycopg 3, pgvector's Python
adapter, Pydantic, and python-dotenv. `requirements.txt` contains the complete
dependency list.