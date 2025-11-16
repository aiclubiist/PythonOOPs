import json
from pathlib import Path
from Database import db
from models import Satellite
from datetime import datetime
from typing import Optional

JSON_FILE = Path(__file__).parent / "satelliteData.json"

def serialize_lists(data):
    
    for key in ("telemetries", "associated_satellites"):
        if isinstance(data.get(key), list):
            data[key] = json.dumps(data[key])
    return data

def parse_iso_datetime(value: Optional[str]) -> Optional[datetime]:
    """Convert ISO8601-like strings (with 'Z' or offset) to datetime, return None for invalid/empty."""
    if value is None:
        return None
    if isinstance(value, (datetime,)):
        return value
    if not isinstance(value, str) or value.strip() == "":
        return None
    try:
        # replace trailing Z with +00:00 so fromisoformat can parse it
        v = value.replace("Z", "+00:00")
        return datetime.fromisoformat(v)
    except Exception:
        # fallback: try parsing date only (YYYY-MM-DD)
        try:
            return datetime.fromisoformat(value)
        except Exception:
            return None

def convert_dates(data):
    """Convert known date fields to Python datetime objects required by SQLAlchemy/SQLite."""
    for key in ("decayed", "launched", "deployed", "updated"):
        if key in data:
            data[key] = parse_iso_datetime(data[key])
    return data

def load_and_insert(json_path=JSON_FILE):
    with open(json_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    if isinstance(payload, dict) and "satellites" in payload:
        items = payload["satellites"]
    elif isinstance(payload, list):
        items = payload
    else:
        raise ValueError("Expected a list or a dict with a 'satellites' list")

    for obj in items:
        data = obj.copy()
        data = serialize_lists(data)
        data = convert_dates(data)
        db.add(Satellite(**data))

    db.commit()
    print(f"Inserted {len(items)} records into the database")

if __name__ == "__main__":
    load_and_insert()