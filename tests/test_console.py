"""Installed launch, Python input recovery, scenario rebinding and CLI options.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import code
import logging
import pathlib
import subprocess
import sys
import sysconfig

import numpy as np
import pytest

import bmi_explorer.app_logging as app_logging
import bmi_explorer.cli as cli
import bmi_explorer.console as console
import bmi_explorer.errors as errors
import bmi_explorer.explorer as teaching
import bmi_explorer.model as model

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.tests.console")


def test_switch_and_reset() -> None:
    """Switching binds a new initialized object; reset also works after finalize.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; verifies console locals and detached pointer lifecycle.
    """
    session: code.InteractiveConsole = console.create("all_grids")
    explorer: teaching.Explorer = session.locals["explorer"]
    previous: model.Model = session.locals["bmi"]
    name: str = "uniform_2d__slope"
    pointer: np.ndarray = previous.get_value_ptr(name)
    pointer[:] = 99
    with pytest.raises(errors.BMIIndexError):
        explorer.use("missing")
    assert session.locals["bmi"] is previous
    explorer.reset()
    current: model.Model = session.locals["bmi"]
    assert current is explorer.bmi and current is not previous
    assert current.get_value_ptr(name)[0] == 0.0124
    np.testing.assert_array_equal(pointer, 99.0)
    with pytest.raises(errors.BMILifecycleError):
        previous.get_current_time()
    assert session.locals["bmi"].get_grid_rank(0) == 0
    explorer.bmi.finalize()
    explorer.reset()
    assert explorer.bmi.get_current_time() == 0.0
    with pytest.raises(TypeError):
        session.locals["scenarios"]["bad"] = "bad"


def test_console_subprocess_outside_checkout(tmp_path: pathlib.Path) -> None:
    """Installed module supports errors, multiline Python, comparisons and clean exit.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param tmp_path: Temporary cwd distinct from the checkout.
    :return: None; verifies actual stdin/stdout and process status.
    """
    source: str = (
        "n = 'uniform_2d__slope'\n"
        "bmi.set_value(n, [1.0])\n"
        "print('RECOVERED', bmi.get_grid_size(bmi.get_var_grid(n)))\n"
        "for i in range(2):\n    print('LOOP', i)\n\n"
        "original = bmi\n"
        "print('COMPARE', 'rectilinear' in explorer.compare(bmi.get_var_grid(n), bmi.get_var_grid('rectilinear_2d__precip_rate')))\n"
        "print('SAME', original is bmi, len(explorer.list()))\n"
        "s = bmi.get_var_grid('scalar__velocity')\n"
        "print('SCALAR', bmi.get_grid_rank(s), bmi.get_grid_size(s))\n"
        "print('HELP', 'BMI REQUIRED' in help_bmi('get_value'))\n"
        "exit()\n"
    )
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [sys.executable, "-m", "bmi_explorer", "--no-banner", "--strict"],
        input=source,
        text=True,
        capture_output=True,
        cwd=tmp_path,
        timeout=20,
        check=False,
    )
    assert result.returncode == 0
    assert "RECOVERED 12" in result.stdout
    assert "LOOP 1" in result.stdout
    assert any(line.endswith("SCALAR 0 1") for line in result.stdout.splitlines())
    assert "HELP True" in result.stdout
    assert "COMPARE True" in result.stdout and "SAME True 9" in result.stdout
    assert "BMITypeError" in result.stderr
    assert "BMI Explorer —" not in result.stderr


@pytest.mark.parametrize(
    "arguments",
    (
        ["--list"],
        ["--scenario", "all_grids", "--no-banner"],
        ["--tour", "buffers", "--no-banner"],
        ["--tour", "scalar", "--no-banner"],
        ["--tour", "grids", "--no-banner"],
    ),
)
def test_installed_entrypoint(tmp_path: pathlib.Path, arguments: list[str]) -> None:
    """The installed console-script entrypoint works outside the checkout, including EOF.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param tmp_path: Independent process cwd.
    :param arguments: Valid CLI options.
    :return: None; verifies normal exit and requested tour/list output.
    """
    executable: pathlib.Path = pathlib.Path(sysconfig.get_path("scripts")) / (
        "bmi-explorer" + (".exe" if sys.platform == "win32" else "")
    )
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [str(executable), *arguments],
        input="",
        text=True,
        capture_output=True,
        cwd=tmp_path,
        timeout=20,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    if "--list" in arguments:
        assert "all_grids:" in result.stdout and "(uniform_2d)" in result.stdout
        assert (
            "(unstructured_mixed)" in result.stdout and "(points_3d)" in result.stdout
        )
    if "--tour" in arguments:
        assert "Valid:" in result.stdout and "Invalid:" in result.stdout


def test_cli_validation() -> None:
    """Only supported scenarios/tours are accepted; relaxed mode is absent.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; verifies parser validation and immutable normalized options.
    """
    options: cli.Options = cli.parse(
        ["--scenario", "all_grids", "--strict", "--no-banner"]
    )
    assert options.scenario == "all_grids" and not options.banner
    option: str
    for option in (
        "--relaxed",
        "--scenario=missing",
        "--scenario=scalar",
        "--scenario=uniform_2d",
        "--tour=missing",
    ):
        with pytest.raises(SystemExit) as error:
            cli.parse([option])
        assert error.value.code == 2
