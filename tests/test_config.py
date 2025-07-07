from bot import config


def test_config_has_values() -> None:
    assert config.OPENROUTER_URL
