import yaml

from typing import Dict


def load_yaml_file(path: str) -> Dict:
    with open(path) as f:
        return yaml.safe_load(f)
