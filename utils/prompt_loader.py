import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROMPT_DIR = os.path.join(BASE_DIR, "core", "prompts")


def load_prompt(name: str):
    path = os.path.join(PROMPT_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
