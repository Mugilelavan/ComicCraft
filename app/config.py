from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    app_name: str = "ComicCraft"
    debug: bool = True

    # Gemini
    gemini_api_key: str = ""
    gemini_flash_model: str = "gemini-3.8-flash"
    gemini_pro_model: str = "gemini-3.1-pro-preview"

    # Hugging Face
    hf_api_key: str = ""
    hf_image_model: str = (
        "stabilityai/stable-diffusion-xl-base-1.0"
    )

    # Image backend:
    # placeholder
    # hf
    # local
    image_backend: str = "placeholder"

    # Local Stable Diffusion
    local_image_model: str = (
        "runwayml/stable-diffusion-v1-5"
    )

    # Image settings
    image_width: int = 768
    image_height: int = 512
    image_steps: int = 25
    image_guidance: float = 7.5

    # Comic
    max_panels: int = 5

    # Folders
    panels_dir: Path = BASE_DIR / "static" / "panels"
    exports_dir: Path = BASE_DIR / "static" / "exports"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()