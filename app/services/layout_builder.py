from app.models import (
    ComicPanel,
    OutlineResponse,
    StoryResponse,
)


def build_comic_layout(
    outline: OutlineResponse,
    story: StoryResponse,
    image_urls: list[str],
) -> list[ComicPanel]:

    if len(outline.panels) != 5:

        raise ValueError(
            "Outline must contain exactly 5 panels."
        )

    if len(story.panels) != 5:

        raise ValueError(
            "Story must contain exactly 5 panels."
        )

    if len(image_urls) != 5:

        raise ValueError(
            "Exactly 5 image URLs are required."
        )

    story_by_number = {
        panel.panel_number: panel
        for panel in story.panels
    }

    result = []

    for (
        outline_panel,
        image_url,
    ) in zip(
        outline.panels,
        image_urls,
    ):

        story_panel = story_by_number.get(
            outline_panel.panel_number
        )

        if story_panel is None:

            raise ValueError(
                "Missing story panel "
                f"{outline_panel.panel_number}"
            )

        result.append(
            ComicPanel(

                panel_number=(
                    outline_panel.panel_number
                ),

                title=outline_panel.title,

                image_url=image_url,

                scene_description=(
                    outline_panel.scene_description
                ),

                caption=story_panel.caption,

                narration=story_panel.narration,

                dialogue=story_panel.dialogue,

                image_prompt=(
                    outline_panel.image_prompt
                ),
            )
        )

    return result