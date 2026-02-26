import json
import pandas as pd
from typing import Dict, Any

def assert_json_safe(obj, context: str = "") -> None:
    json.dumps(obj)

def target_check(df: pd.DataFrame, target: str) -> Dict[str, Any]:
    ...
