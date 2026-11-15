import json
from pathlib import Path

from chunking.pdf_reader import extract_pdf_text
from chunking.strategies import (fixed_size_chunk, heading_based_chunk, recursive_chunk,)

PDF_DIR = Path("data/pdfs")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

strategies = {
    "fixed": fixed_size_chunk,
    "recursive": recursive_chunk,
    "heading": heading_based_chunk,
}

def main():
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if len(pdf_files) != 5:
        raise ValueError(
            f"Expected 5 PDFs, found {len(pdf_files)}"
        )

    all_results = []

    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")

        text = extract_pdf_text(pdf_path)
        if not text.strip():
            print("No extractable text. Skipping.")
            continue

        for strategy_name, chunk_function in strategies.items():
            chunks = chunk_function(text)

            result = {
                "document": pdf_path.name,
                "strategy": strategy_name,
                "chunk_count": len(chunks),
                "chunks": chunks,
            }

            all_results.append(result)

            output_file = (
                OUTPUT_DIR /
                f"{pdf_path.stem}_{strategy_name}.json"
            )

            output_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
            print(
                f"{strategy_name}: {len(chunks)} chunks"
            )

        print(
        f"\nCompleted. Generated {len(all_results)} "
        "document-strategy results.")


if __name__ == "__main__":
    main()
