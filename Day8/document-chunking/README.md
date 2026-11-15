# PDF Document Chunking

A small Python project that extracts text from PDF lecture notes, applies three
chunking strategies, and compares the resulting chunk sizes. It is intended for
learning and experimentation; the heading-based strategy uses a heuristic and
may not identify headings correctly in every document.

## Features

- Extracts text from each PDF page and adds page markers such as `[PAGE 1]`.
- Creates fixed-size, recursive, and heading-based chunks.
- Saves the chunks and document metadata as JSON files.
- Prints summary statistics and writes them to a CSV file.

## Project layout

```text
document-chunking/
  chunking/
    comparison.py    # Summarize generated JSON chunk files
    pdf_reader.py    # Extract text from PDF pages
    strategies.py    # Fixed, recursive, and heading-based chunkers
  data/
    pdfs/            # Input PDF files
  output/            # Generated JSON and CSV files
  main.py            # Run extraction and chunking
  requirements.txt
```

## Setup

Run these commands from the `document-chunking` directory in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Using `python -m pip` avoids relying on the standalone `pip.exe` launcher.

## Run

Place five PDF files in `data/pdfs/`. The current `main.py` expects exactly five
PDF files in that directory. Input PDFs and generated output files are not
included in the repository.

Generate chunks:

```powershell
python -m main
```

This writes one JSON file per PDF and strategy to `output/`. Each JSON file
contains the source document name, strategy name, chunk count, and chunk text.

Generate the comparison table and CSV after the JSON files exist:

```powershell
python -m chunking.comparison
```

The comparison reports each document and strategy's chunk count, average chunk
length, minimum length, and maximum length. It prints a table and writes
`output/comparison.csv`. The comparison uses only Python's standard library.

## Chunking strategies

- **Fixed size**: slices text into 1,000-character chunks with a 150-character
  overlap by default.
- **Recursive**: uses LangChain's `RecursiveCharacterTextSplitter` with the
  same default chunk size and overlap, preferring paragraph, line, and sentence
  boundaries where possible.
- **Heading based**: starts a new chunk when a line matches a numbered-heading
  or uppercase-heading pattern. This is a simple heuristic, not a full document
  structure parser.

The defaults are defined in `chunking/strategies.py` and can be changed when
calling the chunking functions from Python.

## Dependencies

- PyMuPDF (`pymupdf`) for PDF text extraction.
- `langchain-text-splitters` for recursive chunking.
