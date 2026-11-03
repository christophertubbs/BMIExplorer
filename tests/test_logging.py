"""Installed logging defaults, overrides and actionable configuration errors.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import json
import logging
import pathlib

import pytest

import bmi_explorer.app_logging as app_logging
import bmi_explorer.cli as cli

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.tests.logging")


def test_logging_levels(tmp_path: pathlib.Path) -> None:
    """Overrides apply after defaults and can suppress a third-party subsystem.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param tmp_path: Directory for explicit test override JSON.
    :return: None; asserts effective levels and preservation of unrelated loggers.
    """
    override: pathlib.Path = tmp_path / "override.json"
    override.write_text(
        json.dumps(
            {
                "loggers": {
                    "bmi_explorer.console.session": "DEBUG",
                    "example.remote": "ERROR",
                }
            }
        )
    )
    remote: logging.Logger = app_logging.get_logger("example.remote")
    original: int = remote.level
    try:
        app_logging.configure(override)
        assert (
            app_logging.get_logger("bmi_explorer.console.session").getEffectiveLevel()
            == logging.DEBUG
        )
        assert remote.getEffectiveLevel() == logging.ERROR
        assert not remote.disabled
        assert (
            app_logging.get_logger(
                "bmi_explorer.contract.validation"
            ).getEffectiveLevel()
            == logging.WARNING
        )
    finally:
        remote.setLevel(original)
        app_logging.configure()


@pytest.mark.parametrize(
    "text",
    (
        "[",
        "[]",
        "{}",
        '{"loggers": []}',
        '{"loggers": {"__main__": "INFO"}}',
        '{"loggers": {"": "INFO"}}',
        '{"loggers": {"example": "LOUD"}}',
        '{"loggers": {"example": 20}}',
    ),
)
def test_bad_override(tmp_path: pathlib.Path, text: str) -> None:
    """Malformed or unsupported override settings fail explicitly.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param tmp_path: Temporary settings directory.
    :param text: Invalid override file body.
    :return: None; asserts errors are not swallowed.
    """
    path: pathlib.Path = tmp_path / "override.json"
    path.write_text(text)
    with pytest.raises(ValueError):
        app_logging.configure(path)
    assert cli.main(["--log-override", str(path), "--list"]) == 2


def test_missing_override_and_names(tmp_path: pathlib.Path) -> None:
    """An explicit missing file is an error; default absence is valid.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param tmp_path: Directory without an override file.
    :return: None; checks explicit-path and stable-name contracts.
    """
    app_logging.configure()
    with pytest.raises(OSError):
        app_logging.configure(tmp_path / "missing.json")
    with pytest.raises(ValueError):
        app_logging.get_logger("__main__")
    with pytest.raises(ValueError):
        app_logging.get_logger("")
    assert LOGGER.name != "__main__"
