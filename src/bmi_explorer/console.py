"""Python playground with initialized BMI locals and terminal editing.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import code
import logging
import pydoc
import shutil
import sys
import textwrap

import numpy as np

import bmi_explorer.app_logging as app_logging
import bmi_explorer.explorer as teaching
import bmi_explorer.reference as reference
import bmi_explorer.fixtures as fixtures
import bmi_explorer.descriptors as descriptors
import bmi_explorer.terminal as terminal

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.console.session")


def create(scenario: str) -> code.InteractiveConsole:
    """Create an ordinary persistent Python console with teaching helpers.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param scenario: Initial built-in fixture.
    :return: Console with model, teaching helpers, local plain-text help and exit.
    :raises BMIExplorerError: If the selected fixture is invalid.
    """
    namespace: dict[str, object] = {
        "np": np,
        "exit": exit_console,
        "quit": exit_console,
        "help": pydoc.Helper(output=sys.stdout),
    }
    explorer: teaching.Explorer = teaching.Explorer(namespace, scenario)
    namespace.update(
        explorer=explorer, scenarios=fixtures.SCENARIOS, help_bmi=reference.describe
    )
    return terminal.TerminalConsole(namespace)


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
    console: code.InteractiveConsole = create(scenario)
    explorer: teaching.Explorer = console.locals["explorer"]
    if tour is not None:
        explorer.tour(tour)
    text: str = startup_text(explorer, scenario) if banner else ""
    if sys.stdin.isatty() and sys.stdout.isatty():
        console.interact(banner=text, exitmsg="")
    else:
        # Redirected input needs neither terminal control sequences nor editing.
        plain: code.InteractiveConsole = code.InteractiveConsole(console.locals)
        plain.interact(banner=text, exitmsg="")


def startup_text(explorer: teaching.Explorer, scenario: str) -> str:
    """Build readable startup guidance and a compact inventory of the live model.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :param explorer: Teaching helper owning the initialized model.
    :param scenario: Selected fixture name to display.
    :return: Plain text with wrapped prose, grid rows, and executable examples.
    """
    width: int = max(30, min(88, shutil.get_terminal_size().columns))
    rows: list[str] = [
        f"BMI Explorer — {scenario}",
        "Python playground | strict NumPy buffers",
        "",
        "Start here (run each line):",
        "  names = bmi.get_output_var_names()",
        "  print(names)",
        "  n = 'uniform_2d__slope'",
        "  values = np.empty_like(bmi.get_value_ptr(n))",
        "  bmi.get_value(n, values)",
        "  print(values)",
        "",
        "Explore and learn:",
        "  help(bmi.get_value)",
        "  print(help_bmi('get_value'))",
        "  explorer.tour('buffers')",
        "  print(explorer.describe(0))",
        "  explorer.reset()  # restore all initial values",
        "",
        "Available grids (ID: label | BMI type | rank):",
    ]
    names: tuple[str, ...] = tuple(
        dict.fromkeys(
            explorer.bmi.get_output_var_names() + explorer.bmi.get_input_var_names()
        )
    )
    grid_id: int
    for grid_id in dict.fromkeys(explorer.bmi.get_var_grid(name) for name in names):
        grid: descriptors.Grid = explorer.bmi._grid(grid_id, "get_grid_type")
        rows.extend(
            textwrap.wrap(
                f"{grid_id}: {grid.label} | {grid.kind} | rank {grid.rank}",
                width=width,
                initial_indent="  ",
                subsequent_indent="    ",
            )
        )
        rows.extend(
            textwrap.wrap(
                "Variables: "
                + ", ".join(
                    name for name in names if explorer.bmi.get_var_grid(name) == grid_id
                ),
                width=width,
                initial_indent="    ",
                subsequent_indent="      ",
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    rows.append("")
    tip: str
    for tip in (
        "Ready: bmi = initialized model; np = NumPy; explorer = teaching helpers.",
        "Tab completes Python names and quoted BMI variable names. Try bmi. then Tab.",
        "Up/Down: history. Ctrl-R: search history. Right: accept a gray suggestion.",
        "Multiline Python: finish a block with an empty line. Pasting code works too.",
        "Ctrl-C cancels input; Ctrl-D on an empty line or exit() exits.",
        "help() prints in scrollback; scroll up to review. Ctrl-L redraws the screen.",
    ):
        rows.extend(textwrap.wrap(tip, width=width))
    return "\n".join(rows)
