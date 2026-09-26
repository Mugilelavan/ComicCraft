from pydantic import BaseModel, Field


class PromptRequest(BaseModel):

    story_prompt: str = Field(
        ...,
        min_length=5,
        max_length=2000,
    )

    character_name: str = Field(
        ...,
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        ...,
        min_length=1,
        max_length=120,
    )

    tone: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    art_style: str = Field(
        ...,
        min_length=1,
        max_length=80,
    )


class PanelOutline(BaseModel):

    panel_number: int = Field(
        ...,
        ge=1,
        le=5,
    )

    title: str

    scene_description: str

    image_prompt: str


class OutlineResponse(BaseModel):

    panels: list[PanelOutline] = Field(
        ...,
        min_length=5,
        max_length=5,
    )


class PanelStory(BaseModel):

    panel_number: int = Field(
        ...,
        ge=1,
        le=5,
    )

    title: str

    scene_description: str

    caption: str

    narration: str

    dialogue: str


class StoryResponse(BaseModel):

    panels: list[PanelStory] = Field(
        ...,
        min_length=5,
        max_length=5,
    )


class ComicPanel(BaseModel):

    panel_number: int

    title: str

    image_url: str

    scene_description: str

    caption: str

    narration: str

    dialogue: str

    image_prompt: str