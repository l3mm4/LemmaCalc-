# lemma_calc/history.py
import json
from datetime import datetime

HISTORY_FILE = "history.json"


def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
            # Upgrade old entries missing a timestamp
            upgraded = []
            for entry in data:
                if len(entry) == 2:
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    upgraded.append([ts, entry[0], entry[1]])
                else:
                    upgraded.append(entry)
            return upgraded
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: Corrupted history file. Starting with empty history.")
        return []


def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Failed to save history: {e}")
