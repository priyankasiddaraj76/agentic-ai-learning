import csv
import json
from pathlib import Path

OUTPUT_DIR = Path("output")
FIELDS = (
    "document",
    "strategy",
    "chunk_count",
    "average_chars",
    "min_chars",
    "max_chars",
)

def compare_chunks():
    records = []
    for file_path in OUTPUT_DIR.glob("*.json"):
        data = json.loads(file_path.read_text(encoding="utf-8"))

        chunks = data["chunks"]
        lengths = [len(chunk) for chunk in chunks]
        records.append({
            "document": data["document"],
            "strategy": data["strategy"],
            "chunk_count": len(chunks),
            "average_chars": (round(sum(lengths)/len(lengths), 2) if lengths else 0),
            "min_chars": min(lengths) if lengths else 0,
            "max_chars": max(lengths) if lengths else 0,
        })

    records.sort(key=lambda record: (record["document"], record["strategy"]))

    with (OUTPUT_DIR / "comparison.csv").open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

    rows = [[str(record[field]) for field in FIELDS] for record in records]
    widths = [
        max(len(field), *(len(row[index]) for row in rows))
        for index, field in enumerate(FIELDS)
    ]

    print(" | ".join(field.ljust(widths[index]) for index, field in enumerate(FIELDS)))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))

if __name__ == "__main__":
    compare_chunks()