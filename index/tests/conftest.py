"""共享 fixtures。"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_config():
    return {
        "templates": {
            "l1": "\\idx{${key}}",
            "l1Math": "\\idxmath{${sort}}{${display}}",
            "l2": "\\idxsub{${parent}}{${child}}",
        },
        "aliases": {"inverse image": ["preimage"]},
        "math_shortcuts": {},
    }


@pytest.fixture
def simple_entries():
    return [
        {"term": "field", "level": 1, "page": [1]},
        {"term": "inverse function", "level": 1, "page": [20]},
    ]
