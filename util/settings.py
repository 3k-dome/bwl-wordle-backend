import json
from pathlib import Path
from typing import Dict, List


def load_settings_file(filepath: Path) -> Dict[str, str | int | List[Dict[str, str | int]]]:
    with open(filepath, mode="r") as settings_file:
        return json.load(settings_file)
