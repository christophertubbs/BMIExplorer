"""Regression coverage for editing, help output and startup guidance.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
"""

import builtins
import code
import logging
import os
import pydoc
import shutil
import unittest.mock as mock

import prompt_toolkit.completion as completion
import prompt_toolkit.document as document
import pytest

import bmi_explorer.app_logging as app_logging
import bmi_explorer.console as console
import bmi_explorer.terminal as terminal

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.tests.editing")


def candidates(session: code.InteractiveConsole, source: str) -> set[str]:
    """Collect completions at the end of input against a session's live locals.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :param session: Initialized console.
    :param source: Unfinished Python input.
    :return: Candidate replacement strings.
    """
    completer: terminal.PythonCompleter = terminal.PythonCompleter(session.locals)
    return {
        item.text
        for item in completer.get_completions(
            document.Document(source),
            completion.CompleteEvent(completion_requested=True),
        )
    }


def test_live_completion() -> None:
    """Complete Python attributes, user locals and quoted variables after reset.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :return: None; checks live namespace behavior and ordinary metadata completion.
    """
    session: code.InteractiveConsole = console.create("all_grids")
    assert "bmi.get_value(" in candidates(session, "bmi.get_val")
    assert "np.empty(" in candidates(session, "np.empt")
    session.push("my_buffer = np.empty(3)")
    assert "my_buffer" in candidates(session, "my_buff")
    assert "uniform_2d__slope" in candidates(session, "bmi.get_value('uniform_2d")
    assert "get_value" in candidates(session, 'help_bmi("get_val')
    session.push("explorer.reset()")
    assert "bmi.get_value(" in candidates(session, "bmi.get_val")
    assert not candidates(session, " ")


def test_help_stays_in_scrollback(capsys: pytest.CaptureFixture[str]) -> None:
    """Help prints plain text, leaves globals untouched and returns to Python.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :param capsys: Captured terminal streams.
    :return: None; verifies help never opens an external pager.
    """
    original: object = builtins.help
    session: code.InteractiveConsole = console.create("all_grids")
    with mock.patch.object(pydoc, "pager", side_effect=AssertionError("pager opened")):
        session.push("help(bmi.get_value)")
        session.push("help('for')")
        session.push("print('AFTER_HELP', bmi.get_current_time())")
    output: str = capsys.readouterr().out
    assert "get_value" in output and "AFTER_HELP 0.0" in output
    assert "\x1b" not in output and "\x08" not in output
    assert builtins.help is original


def test_startup_inventory() -> None:
    """Banner shows every grid/name, current scenario and printable examples.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :return: None; verifies wrapped inventory prose at a normal terminal width.
    """
    session: code.InteractiveConsole = console.create("all_grids")
    with mock.patch.object(
        shutil, "get_terminal_size", return_value=os.terminal_size((72, 24))
    ):
        text: str = console.startup_text(session.locals["explorer"], "all_grids")
    assert "BMI Explorer — all_grids" in text
    assert "print(help_bmi('get_value'))" in text
    assert "Variables:" in text and "rank 3" in text
    assert all(len(line) <= 72 for line in text.splitlines())
    name: str
    for name in session.locals["bmi"].get_output_var_names():
        assert name in text


@pytest.mark.parametrize(
    "source, expected",
    [
        ("x = 2\ny = 3\nresult = x + y", 5),
        ("for i in range(3):\n    pass\nresult = i", 2),
        ("def double(x):\n    return x * 2\nresult = double(4)\n", 8),
        ("result = (\n2 +\n3\n)", 5),
        ("if False:\n    result = 0\nelse:\n    result = 7", 7),
        ("try:\n    1 / 0\nexcept ZeroDivisionError:\n    result = 9", 9),
    ],
)
def test_bracketed_paste(source: str, expected: int) -> None:
    """Pasted statements and compound blocks execute with normal Python semantics.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :param source: Text delivered as one bracketed paste.
    :param expected: Result set by the pasted code.
    :return: None; checks the pending input queue and compiler integration.
    """
    session: terminal.TerminalConsole = console.create("all_grids")
    session._session = mock.Mock()
    session._session.prompt.side_effect = [source, EOFError()]
    session.interact(banner="", exitmsg="")
    assert session.locals["result"] == expected
