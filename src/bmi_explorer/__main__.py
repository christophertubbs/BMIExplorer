"""Installed module launcher.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import logging

import bmi_explorer.app_logging as app_logging
import bmi_explorer.cli as cli

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.entry.module")

if __name__ == "__main__":
    raise SystemExit(cli.main())
