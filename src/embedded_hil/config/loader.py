
from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

    except FileNotFoundError as exc:
        raise ValueError(
            f"YAML configuration file not found: {path}"
        ) from exc

    except yaml.YAMLError as exc:
        raise ValueError(
            f"Invalid YAML configuration in {path}: {exc}"
        ) from exc

    if config is None:
        raise ValueError(f"YAML configuration file is empty: {path}")

    if not isinstance(config, dict):
        raise ValueError(
            f"YAML configuration must be a mapping: {path}"
        )

    return config
