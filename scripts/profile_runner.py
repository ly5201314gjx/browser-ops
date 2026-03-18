#!/usr/bin/env python3
import json
from pathlib import Path

REQUIRED_KEYS = ["name", "route", "startUrls"]


def load_profile(path: str) -> dict:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    for key in REQUIRED_KEYS:
        if key not in data:
            raise ValueError(f"profile missing required key: {key}")
    return data
