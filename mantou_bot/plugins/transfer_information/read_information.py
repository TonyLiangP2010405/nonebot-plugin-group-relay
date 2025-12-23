import json
from pathlib import Path

_plugin_state = False
STATE_FILE = Path(__file__).parent / "plugin_information.json"


def _load_state():
    global _plugin_state
    if STATE_FILE.exists():
        try:
            _plugin_state = json.loads(STATE_FILE.read_text("utf-8"))
        except Exception:
            _plugin_state = {}
    else:
        _plugin_state = {}


def _save_state():
    STATE_FILE.write_text(
        json.dumps(_plugin_state, ensure_ascii=False, indent=2),
        "utf-8",
    )