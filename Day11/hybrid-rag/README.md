# Day 11: Hybrid RAG

A command-line retrieval-augmented generation project for computational
biology material. It includes semantic vector search, PostgreSQL full-text
search, and Reciprocal Rank Fusion (RRF) to combine ranked search results.
Gemini generates a context-grounded answer with citations.

## How it works

The project has two retrieval paths:

- **Vector search** embeds the question with Gemini's
  `gemini-embedding-001` model and finds nearby document embeddings using
  pgvector's cosine-distance operator (`<=>`).
- **Full-text search** parses the question with PostgreSQL's English
  `websearch_to_tsquery` and ranks matching content using `ts_rank_cd`.
- **Hybrid search** combines the two ranked lists with Reciprocal Rank Fusion:
  each result gains `1 / (RRF_K + rank)` from each list where it appears, then
  the combined results are sorted by score.

The configured embedding size is **768 dimensions**. The stored document
embeddings and question embeddings must use the same model and dimensions.

> **Current CLI behavior:** `python -m src.main` calls the vector retriever
> directly. The hybrid retriever is implemented separately and is used by
> `src.evaluation` to compare vector-only and hybrid results.

## Project layout

```text
hybrid-rag/
  data/                    # Local chunk data; not loaded automatically
  src/
    config.py              # Database, model, and retrieval settings
    embeddings.py          # Gemini query embeddings
    retriever.py           # Vector search
    hybrid_retriever.py    # Full-text search and hybrid orchestration
    rrf.py                 # Reciprocal Rank Fusion
    prompt.py              # Context-grounded prompt
    generator.py           # Gemini answer generation
    validators.py          # Answer and citation validation
    main.py                # Interactive question/answer CLI
    evaluation.py          # Vector vs. hybrid retrieval metrics
  requirements.txt
  schema.sql               # pgvector table and full-text index
```

## Prerequisites

- Python 3.13 or Docker Desktop.
- PostgreSQL with the pgvector extension.
- A Gemini API key with access to the configured embedding and generation
  models.
- A populated `document_chunks` table containing content and 768-dimensional
  embeddings.

**This project does not currently include an ingestion script.** JSON files
under `data/` are not loaded by the CLI. Before searching, insert document
chunks and their embeddings into PostgreSQL. The generated `search_vector`
column is maintained by PostgreSQL from each row's `content`.

## Configure environment

Create a local `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=postgresql://appuser:your-password@localhost:5432/vectordb
```

Replace the connection values with those for your PostgreSQL instance. Keep
`.env` private; it is excluded from Git.

## Initialize the database

`schema.sql` enables pgvector and creates `document_chunks` with:

- `id`: text primary key
- `content`: document text
- `embedding`: 768-dimensional vector
- `metadata`: JSONB metadata
- `search_vector`: generated English full-text representation of `content`

It also creates a GIN index for full-text search. To apply the schema from
PowerShell when PostgreSQL is running in Docker, run this from the project
directory (replace the container, user, or database if needed):

```powershell
Get-Content .\schema.sql | docker exec -i day9-postgre psql -U appuser -d vectordb
```

PowerShell uses a pipe here; `< schema.sql` is not valid PowerShell input
redirection. The schema's `ALTER TABLE ... ADD COLUMN` and `CREATE INDEX`
statements are not idempotent. Apply the schema once per database; inspect the
table before rerunning it.

## Run the application

### Windows with Docker

If Windows Application Control blocks psycopg's native DLL, run Python in a
Linux container. Ensure PostgreSQL is running and accessible from the Python
container. For a database container named `day9-postgre`, run this in
PowerShell from the project directory:

```powershell
docker run --rm -it `
  --network container:day9-postgre `
  --mount "type=bind,source=$($PWD.Path),target=/app" `
  -w /app `
  --env-file .env `
  python:3.13-slim `
  sh -c "pip install --no-cache-dir -r requirements.txt && python -m src.main"
```

The `-it` flags keep the interactive prompt connected. With
`--network container:day9-postgre`, `localhost` in `DATABASE_URL` refers to
that PostgreSQL container's network namespace.

### Local Python environment

If your machine allows psycopg's native driver to load:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.main
```

The CLI asks a question and prints the answer, citations, and retrieved chunk
IDs with similarity scores.

## Evaluate retrieval

Run the evaluation module:

```powershell
python -m src.evaluation
```

The evaluation compares vector-only and hybrid retrieval using Hit Rate@3,
Recall@3, and Mean Reciprocal Rank (MRR). It embeds questions and therefore
requires database access, Gemini API access, and available API quota.

Update `GROUND_TRUTH` in `src/evaluation.py` with the actual relevant chunk IDs
for each question before relying on the metrics. The retrieved IDs and
ground-truth IDs must have matching values and types. `TOP_K` is currently 3,
so the metrics are calculated over the top three results.

## Dependencies

The project uses Google Gen AI (`google-genai`), Psycopg 3, pgvector's Python
adapter, Pydantic, and python-dotenv. See `requirements.txt` for the full
dependency list.
