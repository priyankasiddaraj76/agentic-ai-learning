# The script should:
# 1. Load the 20 tickets.
# 2. Call the LLM for each ticket.
# 3. Compare predicted category with expected category.
# 4. Compare predicted priority with expected priority.
# 5. Print each prediction.
# 6. Calculate classification accuracy.
# 7. Save all predictions into a JSON file.

import json
from classifier import classify_ticket
from sample_tickets import SAMPLE_TICKETS
import time
from pathlib import Path

def main():
    results = []
    category_correct = 0
    priority_correct = 0
    fully_correct = 0

    total = len(SAMPLE_TICKETS)
    output_dir = Path("results")

    output_dir.mkdir(exist_ok=True)

    print("=" * 80)
    print("             AI SUPPORT TICKET CLASSIFICATION")
    print("=" * 80)

    for ticket in SAMPLE_TICKETS:
        ticket_id = ticket["id"]
        message = ticket["message"]

        print(f"\nProcessing Ticket {ticket_id}...")
        print(f"Message: {message}")

        try:
            start_time = time.perf_counter()
            prediction = classify_ticket(message)
            elapsed = time.perf_counter() - start_time

            predicted_category = prediction.category
            predicted_priority = prediction.priority

            expected_category = ticket["expected_category"]
            expected_priority = ticket["expected_priority"]

            category_match = predicted_category == expected_category
            priority_match = predicted_priority == expected_priority

            is_correct = category_match and priority_match

            category_correct += int(category_match)
            priority_correct += int(priority_match)
            fully_correct += int(is_correct)

            result = {
                "id": ticket_id,
                "message": message,
                "expected_category": expected_category,
                "predicted_category": predicted_category,
                "expected_priority": expected_priority,
                "predicted_priority": predicted_priority,
                "summary": prediction.summary,
                "category_correct": category_match,
                "priority_correct": priority_match,
                "fully_correct": is_correct,
                "time_seconds": round(elapsed, 2)
            }

            results.append(result)

            print(f"Category: {predicted_category}")
            print(f"Priority: {predicted_priority}")
            print(f"Summary: {prediction.summary}")

            print(
                "Result:",
                "PASS" if is_correct else "FAIL"
            )
        except Exception as e:
            print(f"Ticket failed: {e}")

            results.append({
                "id": ticket_id,
                "message": message,
                "error": str(e),
                "fully_correct": False
            })

    successful = sum(
        1 for result in results
        if "error" not in result
    )

    def accuracy(correct, denominator):
        if denominator == 0:
            return 0.0
        return (correct / denominator) * 100

    print("\n" + "=" * 80)
    print("                    EVALUATION SUMMARY")
    print("=" * 80)

    print(f"Total tickets: {total}")
    print(f"Successful API calls: {successful}")

    print(
        f"Category accuracy: "
        f"{accuracy(category_correct, successful):.2f}%"
    )

    print(
        f"Priority accuracy: "
        f"{accuracy(priority_correct, successful):.2f}%"
    )

    print(
        f"Exact match accuracy: "
        f"{accuracy(fully_correct, successful):.2f}%"
    )

    output_file = output_dir / "classification.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
