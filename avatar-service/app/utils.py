from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def get_path(*parts: str) -> Path:
    return BASE_DIR.joinpath(*parts)
