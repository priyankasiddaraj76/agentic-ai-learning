# COST CALCULATION
from dataclasses import dataclass

@dataclass
class UsageRecord:
    request_id: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    input_price_per_million: float,
    output_price_per_million: float,
) -> float:
    input_cost = input_tokens * input_price_per_million / 1_000_000
    output_cost = output_tokens * output_price_per_million / 1_000_000

    return round(input_cost + output_cost, 8)
