from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models import PromptRequest
from app.services.exporters import save_pdf
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout


router = APIRouter()


templates = Jinja2Templates(
    directory="templates"
)


# =========================================================
# COMPLETE COMIC PIPELINE
# =========================================================

def run_pipeline(data: PromptRequest):

    # 1. Generate 5-panel outline
    outline = generate_outline(data)

    # 2. Generate detailed story
    story = generate_story(
        data,
        outline,
    )

    # 3. Generate image for every panel
    image_urls = []

    for panel in outline.panels:

        image_url = generate_image(
            panel.image_prompt
        )

        image_urls.append(image_url)

    # 4. Build final layout
    layout = build_comic_layout(
        outline=outline,
        story=story,
        image_urls=image_urls,
    )

    # 5. Export PDF
    pdf_url = save_pdf(layout)

    return layout, pdf_url


# =========================================================
# HOME
# =========================================================

@router.get(
    "/",
    response_class=HTMLResponse,
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": None,
        },
    )


# =========================================================
# GENERATE COMIC - HTML FORM
# =========================================================

@router.post(
    "/generate",
    response_class=HTMLResponse,
)
def generate_comic(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):

    try:

        data = PromptRequest(
            story_prompt=story_prompt.strip(),

            character_name=character_name.strip(),

            setting=setting.strip(),

            tone=tone.strip(),

            art_style=art_style.strip(),
        )

        panels, pdf_url = run_pipeline(data)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "panels": panels,

                "pdf_url": pdf_url,

                "test_image_url": None,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(exc),
            },
            status_code=500,
        )


# =========================================================
# GENERATE COMIC - JSON API
# =========================================================

@router.post(
    "/generate-comic/json"
)
def generate_comic_json(
    data: PromptRequest,
):

    panels, pdf_url = run_pipeline(data)

    return {
        "success": True,

        "panels": [
            panel.model_dump()
            for panel in panels
        ],

        "pdf_url": pdf_url,
    }


# =========================================================
# TEST IMAGE
# =========================================================

@router.post(
    "/test-image",
    response_class=HTMLResponse,
)
def test_image(
    request: Request,

    prompt: str = Form(...),
):

    try:

        prompt = prompt.strip()

        if not prompt:

            raise ValueError(
                "Image prompt cannot be empty."
            )

        image_url = generate_image(
            prompt
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "panels": [],

                "pdf_url": None,

                "test_image_url": image_url,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": str(exc),
            },
            status_code=500,
        )


# =========================================================
# EXPORT SUCCESS
# =========================================================

@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
def export_success(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={},
    )