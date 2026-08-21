import yaml
from datetime import datetime, date

def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def parse_published_date(pub_str: str):
    if not pub_str or pub_str == "NO DATE":
        return None, None, None
    try:
        dt = datetime.strptime(pub_str[:25], "%a, %d %b %Y %H:%M:%S")
        return dt.day, dt.month, dt.year
    except Exception:
        return None, None, None
