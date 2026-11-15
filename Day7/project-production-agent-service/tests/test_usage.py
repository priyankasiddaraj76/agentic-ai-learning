
from app.usage import calculate_cost


def test_calculate_cost():
    result = calculate_cost(
        input_tokens=2000,
        output_tokens=500,
        input_price_per_million=0.75,
        output_price_per_million=3.75,
    )

    assert result == 0.003375


def test_zero_tokens():
    result = calculate_cost(
        input_tokens=0,
        output_tokens=0,
        input_price_per_million=0.75,
        output_price_per_million=3.75,
    )

    assert result == 0.0
