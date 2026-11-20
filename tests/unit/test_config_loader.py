
import pytest
from pathlib import Path

from embedded_hil.config.loader import load_yaml_config


def test_load_yaml_config(tmp_path: Path) -> None:
    config_file = tmp_path / "bench.yaml"
    config_file.write_text(
        "bench:\n"
        "  id: rpi5-bench-01\n",
        encoding="utf-8",
    )

    config = load_yaml_config(config_file)

    assert config["bench"]["id"] == "rpi5-bench-01"

def test_load_yaml_config_rejects_empty_file(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "empty.yaml"
    config_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        load_yaml_config(config_file)

def test_load_yaml_config_rejects_list(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "invalid.yaml"
    config_file.write_text(
        "- relay\n"
        "- camera\n"
        "- uart\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="mapping"):
        load_yaml_config(config_file)

def test_load_yaml_config_rejects_invalid_syntax(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "broken.yaml"
    config_file.write_text(
        "hardware:\n"
        "  relay: [1, 2, 3\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid YAML"):
        load_yaml_config(config_file)

def test_load_yaml_config_missing_file(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "missing.yaml"

    with pytest.raises(ValueError, match="not found"):
        load_yaml_config(config_file)

@pytest.mark.parametrize(
    "filename, expected_key",
    [
        ("bench.rpi5.example.yaml", "bench"),
        ("dut.sentry.example.yaml", "dut"),
        ("vision.example.yaml", "vision"),
    ],
)
def test_load_example_configs(
    filename: str,
    expected_key: str,
) -> None:
    project_root = Path(__file__).resolve().parents[2]
    config_file = project_root / "configs" / filename

    config = load_yaml_config(config_file)

    assert expected_key in config
