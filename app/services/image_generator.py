from uuid import uuid4

from PIL import Image, ImageDraw

from app.config import settings


def _new_filename() -> str:
    return f"panel_{uuid4().hex}.png"


def _placeholder(prompt: str) -> str:
    settings.panels_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = settings.panels_dir / _new_filename()

    image = Image.new(
        "RGB",
        (
            settings.image_width,
            settings.image_height,
        ),
        "white",
    )

    draw = ImageDraw.Draw(image)

    draw.text(
        (30, 30),
        "ComicCraft - Test Image",
        fill="black",
    )

    draw.text(
        (30, 70),
        prompt[:700],
        fill="black",
    )

    image.save(path, "PNG")

    return f"/static/panels/{path.name}"


def _huggingface(prompt: str) -> str:

    if not settings.hf_api_key:
        raise RuntimeError(
            "HF_API_KEY is missing in .env"
        )

    from huggingface_hub import InferenceClient

    client = InferenceClient(
        provider="auto",
        api_key=settings.hf_api_key,
    )

    print("Generating AI image with Hugging Face...")
    print(f"Model: {settings.hf_image_model}")

    image = client.text_to_image(
        prompt=prompt,
        model=settings.hf_image_model,
        width=settings.image_width,
        height=settings.image_height,
        num_inference_steps=settings.image_steps,
        guidance_scale=settings.image_guidance,
    )

    if image is None:
        raise RuntimeError(
            "Hugging Face returned no image."
        )

    settings.panels_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = settings.panels_dir / _new_filename()

    image.save(
        path,
        "PNG",
    )

    print(f"Image saved: {path}")

    return f"/static/panels/{path.name}"


def _local(prompt: str) -> str:

    import torch
    from diffusers import StableDiffusionPipeline

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    dtype = (
        torch.float16
        if device == "cuda"
        else torch.float32
    )

    pipe = StableDiffusionPipeline.from_pretrained(
        settings.local_image_model,
        torch_dtype=dtype,
    )

    pipe = pipe.to(device)

    result = pipe(
        prompt,
        negative_prompt=(
            "blurry, low quality, "
            "distorted face, bad anatomy, "
            "extra fingers, watermark, "
            "logo, text"
        ),
        width=settings.image_width,
        height=settings.image_height,
        num_inference_steps=settings.image_steps,
        guidance_scale=settings.image_guidance,
    )

    settings.panels_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = settings.panels_dir / _new_filename()

    result.images[0].save(
        path,
        "PNG",
    )

    return f"/static/panels/{path.name}"


def generate_image(prompt: str) -> str:

    prompt = prompt.strip()

    if not prompt:
        raise ValueError(
            "Image prompt cannot be empty."
        )

    backend = (
        settings.image_backend
        .strip()
        .lower()
    )

    if backend == "placeholder":
        return _placeholder(prompt)

    if backend == "hf":
        return _huggingface(prompt)

    if backend == "local":
        return _local(prompt)

    raise ValueError(
        "IMAGE_BACKEND must be "
        "placeholder, hf, or local."
    )