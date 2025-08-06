import json
import os

file_path = os.path.join(os.path.dirname(__file__), "../intents.json")
with open(file_path) as f:
    intents = json.load(f)

def get_suggestions(intent_name):
    for item in intents:
        if item["intent"] == intent_name:
            return item.get("suggested_replies", [])
    return []
