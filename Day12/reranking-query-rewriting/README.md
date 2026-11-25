# Day 12: Query Rewriting and Reranking

This project extends a computational-biology RAG pipeline with two retrieval
improvements:

- **Query rewriting** uses Gemini to clarify and expand a user's question for
  search while preserving its intent.
- **Cross-encoder reranking** scores candidate text chunks against the original
  question and sorts the candidates by relevance.

The pipeline combines query rewriting, PostgreSQL vector search, PostgreSQL
full-text search, Reciprocal Rank Fusion (RRF), reranking, and a
context-grounded Gemini answer with validated citations.

## Retrieval pipeline

`python -m src.main` calls `advanced_search` and follows these steps:

1. Rewrite the user's question with Gemini. If rewriting raises an error, the
   original question is used as a fallback.
2. Search the database using both vector similarity and PostgreSQL full-text
   search, using the rewritten query.
3. Merge the ranked candidate lists with Reciprocal Rank Fusion.
4. Rerank the merged candidates with a CrossEncoder, comparing each chunk to
   the original question.
5. Give the top results to Gemini to generate a JSON answer with chunk-ID
   citations.
6. Validate the response and ensure each citation refers to a retrieved chunk.

The configured embedding model is `gemini-embedding-001` with **768 output
dimensions**. The database embeddings and query embeddings must use the same
model and dimensions.

## Retrieval variants

`src/evaluation.py` compares four configurations:

| Variant | Retrieval process |
| --- | --- |
| A - Vector | Vector similarity search |
| B - Hybrid | Vector search + full-text search + RRF |
| C - Hybrid + Rerank | Hybrid candidates reranked against the original question |
| D - Full Day 12 | Rewrite query, hybrid search, then rerank |

The evaluation prints chunk IDs and scores for each question. It does not
compute ground-truth metrics.

## Project layout

```text
reranking-query-rewriting/
  data/                   # Local chunk JSON files; not ingested automatically
  src/
    advanced_retriever.py # Query rewrite -> hybrid retrieval -> reranking
    config.py              # Models and candidate/result limits
    embeddings.py          # Gemini query embeddings
    evaluation.py          # Compare retrieval variants A-D
    generator.py           # Context-grounded Gemini answer generation
    hybrid_retriever.py    # Vector and PostgreSQL full-text search
    main.py                # Interactive RAG CLI
    prompt.py              # Answer prompt and citation instructions
    query_rewriter.py      # Gemini query rewriting
    reranker.py            # CrossEncoder candidate reranking
    retriever.py           # Vector search
    rrf.py                 # Reciprocal Rank Fusion
    validators.py          # Answer and citation validation
  tests/                   # Small runnable examples for rewriting, reranking, RRF
  requirements.txt
  schema.sql               # pgvector and full-text search schema
```

## Prerequisites

- Python 3.13 or Docker Desktop.
- PostgreSQL with the pgvector extension.
- A Gemini API key with access to the configured models.
- A populated `document_chunks` table containing content, 768-dimensional
  embeddings, and a generated full-text search column.
- Internet access on the first CrossEncoder run so its model can be downloaded.

**There is no ingestion script in this project.** The JSON files in `data/` are
not loaded automatically. Populate the database with chunks and their
embeddings before running retrieval. The `search_vector` column is generated
from each row's `content` by PostgreSQL.

## Configure environment

Create a local `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=postgresql://appuser:your-password@localhost:5432/vectordb
```

Use the connection details for your PostgreSQL database. Do not commit `.env`;
it is excluded from Git.

## Initialize the database

`schema.sql` enables pgvector and creates the `document_chunks` table with a
768-dimensional embedding column. It adds a generated `search_vector` column
and a GIN index for full-text search.

From PowerShell in the project directory, apply it to a PostgreSQL container:

```powershell
Get-Content .\schema.sql | docker exec -i day9-postgre psql -U appuser -d vectordb
```

Replace the container, user, or database names as needed. PowerShell uses the
pipe to send the file to `psql`; `< schema.sql` is not valid PowerShell
redirection. The `ALTER TABLE` and `CREATE INDEX` statements are not
idempotent, so inspect the table before applying the schema a second time.

## Run the application

### Windows with Docker

If Windows Application Control blocks psycopg's native DLL, run the app in a
Linux Python container. Ensure PostgreSQL is running and accessible from that
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

The `-it` flags keep the interactive question prompt connected. With
`--network container:day9-postgre`, `localhost` in `DATABASE_URL` refers to
that PostgreSQL container's network namespace.

To run the retrieval comparison instead:

```powershell
docker run --rm `
  --network container:day9-postgre `
  --mount "type=bind,source=$($PWD.Path),target=/app" `
  -w /app `
  --env-file .env `
  python:3.13-slim `
  sh -c "pip install --no-cache-dir -r requirements.txt && python -m src.evaluation"
```

The reranker downloads and initializes its CrossEncoder model on first use,
which can take extra time and disk space.

### Local Python environment

If your Python environment can load psycopg's native driver:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.main
```

Run the evaluation with:

```powershell
.\.venv\Scripts\python.exe -m src.evaluation
```

## Configuration

Candidate and result limits and model names are in `src/config.py`:

- `VECTOR_CANDIDATES`: vector-search candidate count.
- `FULLTEXT_CANDIDATES`: full-text-search candidate count.
- `RERANK_CANDIDATES`: maximum RRF results passed to the reranker.
- `FINAL_TOP_K`: number of reranked chunks sent to answer generation.
- `RRF_K`: RRF smoothing constant.
- `RERANKER_MODEL`: Sentence Transformers CrossEncoder model.

## Dependencies

See `requirements.txt` for the full list. The project uses Google Gen AI,
Psycopg 3, pgvector's Python adapter, Pydantic, python-dotenv, Sentence
Transformers, and PyTorch.
