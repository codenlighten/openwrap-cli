"""Quick test to see what the API is returning"""

import json
from pathlib import Path
from lumen_sdk import LumenClient

# Load config
config_path = Path.home() / ".lumen" / "config.json"
with open(config_path) as f:
    config = json.load(f)
    token = config.get("token")

client = LumenClient(token)

print("Testing API response...")
result = client.query(
    "What is 2+2?",
    model="gpt-5-nano",
    temperature=1.0
)

print(f"\nResult type: {type(result)}")
print(f"Result: {result}")
print(f"\nKeys: {result.keys() if isinstance(result, dict) else 'N/A'}")

if isinstance(result, dict):
    for key, value in result.items():
        print(f"  {key}: {type(value)} = {value[:100] if isinstance(value, str) else value}")
