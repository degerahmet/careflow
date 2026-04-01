from pathlib import Path

_PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts" / "agent"


def _load(filename: str) -> str:
    return (_PROMPTS_DIR / filename).read_text(encoding="utf-8")


EXTRACTION_SYSTEM = _load("01_extraction_system.txt")
EXTRACTION_USER   = _load("02_extraction_user.txt")
REPLY_SYSTEM      = _load("03_reply_system.txt")
REPLY_USER        = _load("04_reply_user.txt")
