
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter


def fixed_size_chunk(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def recursive_chunk(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    return splitter.split_text(text)


def heading_based_chunk(text: str) -> list[str]:
    """
    Split on likely numbered or uppercase headings.
    This is a heuristic, not a universal PDF parser.
    """

    # This recognizes some numbered headings such as "2. Installation" and uppercase headings such as "INSTALLATION".
    heading_pattern = re.compile(
        r"^(?:"
        r"\d+(?:\.\d+)*[.)]?\s+.{2,}"
        r"|[A-Z][A-Z0-9\s,:()&/-]{5,}"
        r")$"
    )

    lines = text.splitlines()

    chunks = []
    current_chunk = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        is_heading = bool(
            heading_pattern.match(stripped)
        )

        if is_heading and current_chunk:
            chunks.append(
                "\n".join(current_chunk).strip()
            )
            current_chunk = []

        current_chunk.append(stripped)

    if current_chunk:
        chunks.append(
            "\n".join(current_chunk).strip()
        )

    return chunks
