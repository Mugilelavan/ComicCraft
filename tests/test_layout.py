from app.models import (
    OutlineResponse,
    PanelOutline,
    PanelStory,
    StoryResponse,
)

from app.services.layout_builder import (
    build_comic_layout,
)


def test_build_comic_layout():

    outline = OutlineResponse(

        panels=[

            PanelOutline(

                panel_number=i,

                title=f"Title {i}",

                scene_description=(
                    f"Scene {i}"
                ),

                image_prompt=(
                    f"Image {i}"
                ),
            )

            for i in range(1, 6)
        ]
    )


    story = StoryResponse(

        panels=[

            PanelStory(

                panel_number=i,

                title=f"Title {i}",

                scene_description=(
                    f"Scene {i}"
                ),

                caption=f"Caption {i}",

                narration=f"Narration {i}",

                dialogue=f"Dialogue {i}",
            )

            for i in range(1, 6)
        ]
    )


    images = [

        f"/static/panels/{i}.png"

        for i in range(1, 6)
    ]


    result = build_comic_layout(

        outline,

        story,

        images,
    )


    assert len(result) == 5

    assert result[0].panel_number == 1

    assert result[-1].panel_number == 5