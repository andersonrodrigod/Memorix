import json
from pathlib import Path
from datetime import datetime


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "memoria.json"


def load_memoria() -> list:
    if not DATA_PATH.exists():
        return []

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []



def save_memoria(data: list) -> None:
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_id(data: list) -> int:
    if not data:
        return 1
    return max(item["id"] for item in data) + 1


def parse_tags(tags_text: str) -> list[str]:
    return [
        tag.strip().lower()
        for tag in tags_text.split(",")
        if tag.strip()
    ]


def add_entry(entry: dict) -> None:
    data = load_memoria()

    now = datetime.now().isoformat(timespec="seconds")

    entry["id"] = generate_id(data)
    entry["created_at"] = now
    entry["updated_at"] = now

    data.append(entry)
    save_memoria(data)
