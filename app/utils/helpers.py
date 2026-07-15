
"""Utility helper functions."""

import re
import json
from typing import Dict, Any


def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()


def parse_json_safely(text: str) -> Dict[str, Any]:
    """Parse JSON safely from potentially malformed text."""
    if not text:
        return {}
    
    # Try to find JSON in the text
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except:
            pass
    
    return {}