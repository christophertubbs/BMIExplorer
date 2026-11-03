"""Central logging factory and installed configuration loading.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import importlib.resources
import importlib.resources.abc
import json
import logging
import logging.config
import pathlib


def get_logger(name: str) -> logging.Logger:
    """Return a stable subsystem logger without configuring the host.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param name: Explicit dotted subsystem name.
    :return: Named logger.
    :raises ValueError: If the name is empty or __main__.
    """
    if not name or name == "__main__":
        raise ValueError("Use an explicit subsystem logger name.")
    return logging.getLogger(name)


LOGGER: logging.Logger = get_logger("bmi_explorer.infrastructure.logging")


def configure(override: pathlib.Path | None = None) -> None:
    """Load packaged defaults, then optional explicit level overrides.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param override: Explicit JSON override file; None skips overrides.
    :return: None; configures application logging.
    :raises OSError: If an explicit file cannot be read.
    :raises ValueError: If JSON or logger levels are invalid.
    """
    resource: importlib.resources.abc.Traversable = importlib.resources.files(
        "bmi_explorer"
    ).joinpath("config/log_config.json")
    base: dict[str, object] = json.loads(resource.read_text(encoding="utf-8"))
    levels: dict[str, int] = {}
    data: object
    name: str
    level: object
    numeric: int | None
    if override is not None:
        data = json.loads(override.read_text(encoding="utf-8"))
        if (
            not isinstance(data, dict)
            or set(data) != {"loggers"}
            or not isinstance(data["loggers"], dict)
        ):
            raise ValueError('Logging override must be {"loggers": {"name": "LEVEL"}}.')
        for name, level in data["loggers"].items():
            if not isinstance(name, str) or not name or name == "__main__":
                raise ValueError(
                    "Override logger names must be nonempty and not __main__."
                )
            numeric = (
                logging.getLevelNamesMapping().get(level)
                if isinstance(level, str)
                else None
            )
            if numeric is None:
                raise ValueError(
                    f"Invalid logging level {level!r} for {name!r}; use DEBUG, INFO, WARNING, ERROR or CRITICAL."
                )
            levels[name] = numeric
    logging.config.dictConfig(base)
    for name, numeric in levels.items():
        logging.getLogger(name).setLevel(numeric)
