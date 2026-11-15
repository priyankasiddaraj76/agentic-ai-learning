# RETRY HANDLING

import logging

from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

logger = logging.getLogger(__name__)


def is_retryable(exc: Exception) -> bool:
    if isinstance(exc, (TimeoutError, ConnectionError)):
        return True

    # Provider exceptions can expose a numeric HTTP status
    status = (
        getattr(exc, "code", None)
        or getattr(exc, "status_code", None)
    )

    return status in {429, 500, 502, 503, 504}


def retry_llm_call(function):
    return retry(
        retry=retry_if_exception(is_retryable),
        wait=wait_exponential_jitter(
            initial=1,
            max=8,
        ),
        stop=stop_after_attempt(4),
        before_sleep=lambda state: logger.warning(
            "Retrying LLM request. Attempt %s",
            state.attempt_number + 1,
        ),
        reraise=True,
    )(function)
