from pathlib import Path
from uuid import uuid4

from fpdf import FPDF

from app.config import BASE_DIR, settings
from app.models import ComicPanel


def _safe_pdf_text(value: str) -> str:
    """
    Convert text to PDF-safe Latin-1 text.
    Unsupported Unicode characters are replaced.
    """
    text = str(value)

    return (
        text
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def _break_long_words(text: str, max_length: int = 70) -> str:
    """
    Add spaces into very long words/URLs so fpdf2
    can wrap them safely.
    """

    words = text.split(" ")
    result = []

    for word in words:

        if len(word) <= max_length:
            result.append(word)
            continue

        chunks = [
            word[i:i + max_length]
            for i in range(0, len(word), max_length)
        ]

        result.append(" ".join(chunks))

    return " ".join(result)


def _prepare_text(value: str) -> str:
    """
    Prepare AI-generated text safely for PDF.
    """

    text = _safe_pdf_text(value)

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = _break_long_words(text)

    return text.strip()


def _image_path(image_url: str) -> Path:
    """
    Convert /static/panels/example.png
    into the actual local filesystem path.
    """

    clean_url = image_url.lstrip("/")

    parts = clean_url.split("/")

    return BASE_DIR.joinpath(*parts)


def _write_text(
    pdf: FPDF,
    heading: str,
    value: str,
):
    """
    Safely write a heading and paragraph.
    """

    heading_text = _prepare_text(heading)
    value_text = _prepare_text(value)

    pdf.set_font("Helvetica", "B", 10)

    pdf.multi_cell(
        w=pdf.epw,
        h=6,
        text=heading_text,
    )

    pdf.set_font("Helvetica", "", 10)

    if value_text:
        pdf.multi_cell(
            w=pdf.epw,
            h=6,
            text=value_text,
        )

    pdf.ln(1)


def save_pdf(panels: list[ComicPanel]) -> str:

    if not panels:
        raise ValueError(
            "Cannot create PDF from empty comic."
        )

    settings.exports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_margins(
        left=15,
        top=15,
        right=15,
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for panel in panels:

        pdf.add_page()

        # -----------------------------
        # PANEL TITLE
        # -----------------------------

        pdf.set_font(
            "Helvetica",
            "B",
            16,
        )

        title = _prepare_text(
            f"Panel {panel.panel_number}: "
            f"{panel.title}"
        )

        pdf.multi_cell(
            w=pdf.epw,
            h=10,
            text=title,
        )

        # -----------------------------
        # PANEL IMAGE
        # -----------------------------

        image_path = _image_path(
            panel.image_url
        )

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=15,
                y=35,
                w=180,
                h=105,
            )

            pdf.set_y(145)

        else:

            pdf.set_font(
                "Helvetica",
                "",
                10,
            )

            pdf.multi_cell(
                w=pdf.epw,
                h=6,
                text="Image not available.",
            )

        # -----------------------------
        # PANEL TEXT
        # -----------------------------

        _write_text(
            pdf,
            "Scene Description",
            panel.scene_description,
        )

        _write_text(
            pdf,
            "Caption",
            panel.caption,
        )

        _write_text(
            pdf,
            "Narration",
            panel.narration,
        )

        _write_text(
            pdf,
            "Dialogue",
            panel.dialogue,
        )

    # -----------------------------
    # SAVE PDF
    # -----------------------------

    filename = (
        f"comic_{uuid4().hex}.pdf"
    )

    output = (
        settings.exports_dir
        / filename
    )

    pdf.output(str(output))

    return (
        f"/static/exports/{filename}"
    )