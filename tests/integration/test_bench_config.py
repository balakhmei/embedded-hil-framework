
from pathlib import Path

from embedded_hil.config.loader import load_yaml_config
from embedded_hil.config.validation import validate_bench_config


def test_rpi5_example_config_is_valid() -> None:
    project_root = Path(__file__).resolve().parents[2]

    config_path = (
        project_root
        / "configs"
        / "bench.rpi5.example.yaml"
    )

    config = load_yaml_config(config_path)

    validate_bench_config(config)
