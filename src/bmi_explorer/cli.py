"""Argument boundary and application composition for the installed console.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import argparse
import dataclasses
import logging
import pathlib

import bmi_explorer.app_logging as app_logging
import bmi_explorer.descriptors as descriptors
import bmi_explorer.console as console
import bmi_explorer.fixtures as fixtures
import bmi_explorer.explorer as teaching

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.cli.lifecycle")


@dataclasses.dataclass(frozen=True, slots=True)
class Options:
    """Normalized CLI settings; strict buffers are always enforced.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param scenario: Initial fixture name.
    :param list_scenarios: Whether to list all grids in the scenario and exit.
    :param tour: Explicitly requested introductory tour.
    :param banner: Whether to display the startup banner.
    :param log_override: Optional explicit infrastructure override file.
    """

    scenario: str
    list_scenarios: bool
    tour: str | None
    banner: bool
    log_override: pathlib.Path | None


def parse(argv: list[str] | None = None) -> Options:
    """Parse CLI arguments into immutable settings.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param argv: Argument strings, or None to consume process arguments.
    :return: Validated application options.
    :raises SystemExit: For help or invalid command-line arguments.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Explore strict CSDMS BMI fixtures interactively."
    )
    parser.add_argument(
        "--scenario",
        choices=tuple(fixtures.SCENARIOS),
        default=descriptors.DEFAULT_SCENARIO,
    )
    parser.add_argument("--list", action="store_true", dest="list_scenarios")
    parser.add_argument("--tour", choices=("scalar", "buffers", "grids"))
    parser.add_argument("--no-banner", action="store_true")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Make default strict buffer enforcement explicit.",
    )
    parser.add_argument(
        "--log-override", type=pathlib.Path, help="Explicit JSON logging override file."
    )
    args: argparse.Namespace = parser.parse_args(argv)
    return Options(
        args.scenario,
        args.list_scenarios,
        args.tour,
        not args.no_banner,
        args.log_override,
    )


def main(argv: list[str] | None = None) -> int:
    """Initialize logging and dispatch one installed command.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param argv: Arguments, or None for process arguments.
    :return: Zero on normal completion; two on invalid logging configuration.
    :raises SystemExit: For argparse help/errors or interactive exit().
    """
    options: Options = parse(argv)
    try:
        app_logging.configure(options.log_override)
    except (OSError, ValueError) as exc:
        LOGGER.error("Cannot configure logging: %s", exc)
        return 2
    if options.list_scenarios:
        explorer: teaching.Explorer = teaching.Explorer({}, options.scenario)
        print(f"{options.scenario}: {fixtures.SCENARIOS[options.scenario].description}")
        print("\n".join(explorer.list().values()))
        return 0
    console.run(options.scenario, options.banner, options.tour)
    return 0
