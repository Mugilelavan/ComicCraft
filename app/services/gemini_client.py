import time

from google import genai

from app.config import settings


def get_gemini_client() -> genai.Client:
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing in .env"
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_with_retry(
    client,
    model,
    contents,
    config,
    max_retries=4,
):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )

        except Exception as exc:
            error_text = str(exc)

            is_retryable = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            )

            if not is_retryable:
                raise

            if attempt == max_retries - 1:
                raise RuntimeError(
                    "Gemini API is temporarily busy. "
                    "Please try again after a short while."
                ) from exc

            delay = 3 * (2 ** attempt)

            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {delay} seconds..."
            )

            time.sleep(delay)