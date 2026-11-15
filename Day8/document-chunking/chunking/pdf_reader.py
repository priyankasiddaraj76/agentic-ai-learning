
import fitz
from pathlib import Path


def extract_pdf_text(pdf_path: Path) -> str:
    """
    Extract text from every page of a PDF.
    Add page markers so we can trace chunks back to their source pages.
    """
    extracted_pages = []

    # opens the pdf
    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            # extracts text from each page
            page_text = page.get_text("text")

            if page_text.strip():
                extracted_pages.append(
                    f"\n[PAGE {page_number}]\n{page_text}"
                )

    return "\n".join(extracted_pages)
