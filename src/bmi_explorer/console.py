"""Standard Python interactive console with initialized BMI locals.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import code
import logging

import numpy as np

import bmi_explorer.app_logging as app_logging
import bmi_explorer.explorer as teaching
import bmi_explorer.reference as reference
import bmi_explorer.fixtures as fixtures

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.console.session")


def create(scenario: str) -> code.InteractiveConsole:
    """Create an ordinary persistent Python console with teaching helpers.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param scenario: Initial built-in fixture.
    :return: Console with np, bmi, explorer, scenarios, help_bmi, and exit locals.
    :raises BMIExplorerError: If the selected fixture is invalid.
    """
    namespace: dict[str, object] = {
        "np": np,
        "exit": exit_console,
        "quit": exit_console,
    }
    explorer: teaching.Explorer = teaching.Explorer(namespace, scenario)
    namespace.update(
        explorer=explorer, scenarios=fixtures.SCENARIOS, help_bmi=reference.describe
    )
    return code.InteractiveConsole(namespace)


def exit_console() -> None:
    """Exit the local interactive process.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: Does not return.
    :raises SystemExit: Always, with successful status.
    """
    raise SystemExit(0)


def run(scenario: str, banner: bool, tour: str | None) -> None:
    """Launch a preloaded console; ordinary errors remain recoverable.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param scenario: Built-in initial fixture.
    :param banner: Whether to show the brief teaching banner.
    :param tour: Optional explicitly requested introductory tour.
    :return: None after EOF; user exit() raises SystemExit.
    :raises BMIExplorerError: If fixture setup fails.
    """
    try:
        import readline  # Optional standard-library history/editing on supported runtimes.
    except ImportError:
        LOGGER.debug("Readline is unavailable; using standard console input.")
    console: code.InteractiveConsole = create(scenario)
    explorer: teaching.Explorer = console.locals["explorer"]
    if tour is not None:
        explorer.tour(tour)
    text: str = (
        (
            "BMI Explorer — all_grids, strict buffers. Grid inventory:\n"
            + "\n".join(explorer.list().values())
            + "\nTry explorer.list(), help_bmi('get_value'), explorer.tour('buffers')."
            + "\nUse explorer.compare(a, b) or explorer.reset(); exit() or EOF exits."
        )
        if banner
        else ""
    )
    console.interact(banner=text, exitmsg="")
