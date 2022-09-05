from flask import Flask
from .database import load_words, setup_difficulties
from .settings import load_settings_file

def print_map(app: Flask) -> None:
    """Utility to print all available routes at startup."""
    print("Routes:".ljust(59, "-"))
    for rule in app.url_map.iter_rules():
        print(f"{rule}".ljust(25), "\t", rule.methods)
    print("-" * 59, end="\n\n")
