from google.genai import types

from app.config import settings
from app.models import (
    OutlineResponse,
    PromptRequest,
    StoryResponse,
)
from app.services.gemini_client import (
    generate_with_retry,
    get_gemini_client,
)


def generate_story(
    data: PromptRequest,
    outline: OutlineResponse,
) -> StoryResponse:

    client = get_gemini_client()

    outline_text = "\n\n".join(
        [
            (
                f"Panel {panel.panel_number}: "
                f"{panel.title}\n"
                f"Scene: {panel.scene_description}"
            )
            for panel in outline.panels
        ]
    )

    prompt = f"""
Expand the following comic outline into
a complete 5-panel comic script.

Story:
{data.story_prompt}

Character:
{data.character_name}

Setting:
{data.setting}

Tone:
{data.tone}

OUTLINE:

{outline_text}

Requirements:

1. Return exactly 5 panels.
2. Panel numbers must be 1 through 5.
3. Keep the same story continuity.
4. Keep the character consistent.
5. Create a caption for every panel.
6. Create narration for every panel.
7. Create natural dialogue for every panel.
8. Keep dialogue concise.
"""

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=StoryResponse,
    )

    response = generate_with_retry(
        client=client,
        model=settings.gemini_pro_model,
        contents=prompt,
        config=config,
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty story."
        )

    result = StoryResponse.model_validate_json(
        response.text
    )

    numbers = [
        panel.panel_number
        for panel in result.panels
    ]

    if numbers != [1, 2, 3, 4, 5]:
        raise RuntimeError(
            f"Invalid story panel numbers returned: {numbers}"
        )

    return result