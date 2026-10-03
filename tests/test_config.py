import pathlib

import pytest

from dank.config import ConfigError, load_settings


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ("", False),
        ("[rss]\nfeed_staleness_days = 7\n", False),
        ("[rss]\nkeep_feed_on_fetch_failure = false\n", False),
        ("[rss]\nkeep_feed_on_fetch_failure = true\n", True),
    ],
)
def test_load_feed_failure_retention_setting(
    *,
    tmp_path: pathlib.Path,
    config: str,
    expected: bool,
) -> None:
    config_path = tmp_path / "test-settings.toml"
    config_path.write_text(config)

    settings = load_settings(config_path)

    assert settings.keep_feed_on_fetch_failure is expected


@pytest.mark.parametrize("value", ['"false"', "1"])
def test_feed_failure_retention_requires_boolean(
    tmp_path: pathlib.Path,
    value: str,
) -> None:
    config_path = tmp_path / "test-settings.toml"
    config_path.write_text(f"[rss]\nkeep_feed_on_fetch_failure = {value}\n")

    with pytest.raises(ConfigError, match="must be a boolean"):
        load_settings(config_path)
