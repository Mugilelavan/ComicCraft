from google.genai import types

from app.config import settings
from app.models import OutlineResponse, PromptRequest
from app.services.gemini_client import (
    generate_with_retry,
    get_gemini_client,
)


def generate_outline(
    data: PromptRequest,
) -> OutlineResponse:

    client = get_gemini_client()

    prompt = f"""
Create a coherent 5-panel comic outline.

Story idea:
{data.story_prompt}

Main character:
{data.character_name}

Setting:
{data.setting}

Tone:
{data.tone}

Art style:
{data.art_style}

Requirements:

1. Return exactly 5 panels.
2. Panel numbers must be 1, 2, 3, 4, 5.
3. Every panel needs a title.
4. Every panel needs a scene description.
5. Every panel needs a detailed image prompt.
6. Keep character consistency.
7. Keep story continuity.
8. Keep the requested art style.
9. Do not put dialogue inside image_prompt.
"""

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=OutlineResponse,
    )

    response = generate_with_retry(
        client=client,
        model=settings.gemini_flash_model,
        contents=prompt,
        config=config,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty outline."
        )

    result = OutlineResponse.model_validate_json(
        response.text
    )

    numbers = [
        panel.panel_number
        for panel in result.panels
    ]

    if numbers != [1, 2, 3, 4, 5]:
        raise RuntimeError(
            f"Invalid panel numbers returned: {numbers}"
        )

    return result