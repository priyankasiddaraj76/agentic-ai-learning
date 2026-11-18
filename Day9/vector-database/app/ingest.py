import json
import re
from pathlib import Path

from app.db import get_connection
from app.embeddings import generate_document_embeddings

CHUNK_DIR = Path("data/chunks")
BATCH_SIZE=32 #sets how many chunks are sent to the embedding API at a time.

def extract_metadata(chunk: str) -> tuple[int | None, str]:
    # Find the first page marker in the chunk
    page_match = re.search(r"\[PAGE\s+(\d+)\]", chunk)

    page = (int (page_match.group(1)) if page_match
            else None)

    # Basic heading detection
    heading_pattern = re.compile(
        r"^(?:"
        r"\d+(?:\.\d+)*[.)]?\s+.{2,}"
        r"|[A-Z][A-Z0-9\s,:()&/-]{5,}"
        r")$"
    )

    section = "Unspecified"

    for line in chunk.splitlines():
        line = line.strip()

        if line.startswith("[PAGE"):
            continue

        if heading_pattern.match(line):
            section = line
            break

    return page, section

def vector_to_string(vector: list[float]) -> str:
    return "[" + ",".join(
        str(float(value)) for value in vector
    ) + "]"

def ingest_file(json_file: Path):
    data = json.loads(json_file.read_text(encoding="utf-8"))

    source = data["document"]
    strategy = data["strategy"]
    chunks = data["chunks"]

    print(f"\nIngesting {source}")
    print(f"Strategy: {strategy}")
    print(f"Chunks: {len(chunks)}")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            for start in range(0, len(chunks), BATCH_SIZE):
                batch = chunks[start:start+BATCH_SIZE]

                embeddings = generate_document_embeddings(batch)

                for offset, (chunk, embedding) in enumerate(zip(batch, embeddings)):
                    chunk_index = start + offset
                    page, section = extract_metadata(chunk)

                    cursor.execute(
                        """
                        INSERT INTO document_chunks (
                            content,
                            embedding,
                            source,
                            page,
                            section,
                            chunk_index,
                            strategy
                        )
                        VALUES (
                            %s,
                            %s::vector,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                        ON CONFLICT (
                            source,
                            strategy,
                            chunk_index
                        )
                        DO UPDATE SET
                            content = EXCLUDED.content,
                            embedding = EXCLUDED.embedding,
                            page = EXCLUDED.page,
                            section = EXCLUDED.section,
                            created_at = NOW()
                        """,
                        (
                            chunk,
                            vector_to_string(embedding),
                            source,
                            page,
                            section,
                            chunk_index,
                            strategy,
                        ),
                    )

                print(
                    f"Processed {start + len(batch)} "
                    f"/ {len(chunks)} chunks"
                )
    print(f"Completed: {source}")

def main():
    json_files = sorted(
        CHUNK_DIR.glob("*_recursive.json")
    )

    if not json_files:
        raise FileNotFoundError(
            "No recursive chunk JSON files found"
        )

    for json_file in json_files:
        ingest_file(json_file)

    print("\nAll documents ingested successfully!")


if __name__ == "__main__":
    main()
