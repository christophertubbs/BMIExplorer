"""Keep the independent browser baseline consistent with Python fixture metadata.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import dataclasses
import json
import logging
import pathlib

import bmi_explorer.app_logging as app_logging
import bmi_explorer.fixtures as fixtures

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.tests.web_fixture_parity")


def test_browser_baseline_matches_python() -> None:
    """Compare every coordinate, connectivity entry and variable descriptor.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; detects fixture drift without running any browser Python bridge.
    """
    path: pathlib.Path = (
        pathlib.Path(__file__).resolve().parents[1] / "web_demo" / "fixtures.js"
    )
    source: str = path.read_text()
    payload: str = source.split("export const BASELINE = ", 1)[1].removesuffix(";\n")
    expected: object = json.loads(
        json.dumps(dataclasses.asdict(fixtures.SCENARIOS["all_grids"]))
    )
    assert json.loads(payload) == expected
