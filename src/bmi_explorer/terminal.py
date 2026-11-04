"""Terminal editing for the ordinary Python console.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
"""

import code
import collections
import collections.abc as generic
import logging
import re
import rlcompleter
import typing

import prompt_toolkit.auto_suggest as suggestions
import prompt_toolkit.completion as completion
import prompt_toolkit.document as document
import prompt_toolkit.lexers as lexers
import prompt_toolkit.layout.processors as processors
import prompt_toolkit.shortcuts as shortcuts
import pygments.lexers.python as python_lexers

import bmi_explorer.app_logging as app_logging
import bmi_explorer.reference as reference
import bmi_explorer.model as model

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.console.editing")


class PythonCompleter(completion.Completer):
    """Complete the live namespace and quoted fixture/method names on Tab.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :param namespace: Live console locals, including the replaceable bmi binding.
    """

    _namespace: dict[str, object]

    def __init__(self, namespace: dict[str, object]) -> None:
        """Retain the live namespace without copying it.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.

        :param namespace: Python globals to complete against.
        :return: None.
        """
        self._namespace = namespace

    def get_completions(
        self, doc: document.Document, complete_event: completion.CompleteEvent
    ) -> generic.Iterator[completion.Completion]:
        """Yield ordinary Python names or quoted BMI teaching names.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.

        :param doc: Current editable input and cursor location.
        :param complete_event: Prompt toolkit's completion request.
        :return: Matching replacements; never invokes a BMI operation.
        """
        quoted: re.Match[str] | None = re.search(
            r"(['\"])(\w*)$", doc.text_before_cursor
        )
        if quoted is not None:
            prefix: str = quoted.group(2)
            bmi: model.Model = typing.cast(model.Model, self._namespace["bmi"])
            # Metadata remains available for completion even after finalize().
            names: set[str] = set(bmi._variables) | set(reference.operations())
            names.update(("scalar", "buffers", "grids", "all_grids"))
            name: str
            for name in sorted(names):
                if name.startswith(prefix):
                    yield completion.Completion(name, start_position=-len(prefix))
            return
        word: str = doc.get_word_before_cursor(pattern=re.compile(r"[\w.]+"))
        if not word:
            return
        completer: rlcompleter.Completer = rlcompleter.Completer(self._namespace)
        index: int = 0
        candidate: str | None = completer.complete(word, index)
        while candidate is not None:
            yield completion.Completion(candidate, start_position=-len(word))
            index += 1
            candidate = completer.complete(word, index)


class TerminalConsole(code.InteractiveConsole):
    """Use prompt toolkit input while preserving Python's execution loop.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :param namespace: Initialized Python locals shared with the teaching helpers.
    """

    _session: shortcuts.PromptSession[str] | None
    _pasted: collections.deque[str]

    def __init__(self, namespace: dict[str, object]) -> None:
        """Create a console; acquire terminal resources only when input starts.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.

        :param namespace: Live console globals.
        :return: None.
        """
        super().__init__(namespace)
        self._session = None
        self._pasted = collections.deque()

    def raw_input(self, prompt: str = "") -> str:
        """Read edited Python or feed bracketed paste through the normal compiler.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.

        :param prompt: Primary or continuation prompt from InteractiveConsole.
        :return: One source line, without its trailing newline.
        :raises EOFError: On Ctrl-D at an empty prompt.
        :raises KeyboardInterrupt: On Ctrl-C; pending pasted input is discarded.
        """
        if self._session is None:
            self._session = shortcuts.PromptSession(
                lexer=lexers.PygmentsLexer(python_lexers.PythonLexer),
                completer=PythonCompleter(self.locals),
                complete_while_typing=False,
                input_processors=[processors.HighlightMatchingBracketProcessor()],
                auto_suggest=suggestions.AutoSuggestFromHistory(),
                reserve_space_for_menu=0,
            )
        try:
            if not self._pasted:
                text: str = self._session.prompt(prompt)
                if "\n" not in text:
                    return text
                self._pasted.extend(text.splitlines())
                self._pasted.append("")
            # Finish a pasted compound statement before the next top-level line.
            if (
                self.buffer
                and self._pasted[0]
                and not self._pasted[0][0].isspace()
                and re.match(r"(?:elif|else|except|finally)\b", self._pasted[0]) is None
            ):
                try:
                    if self.compile("\n".join(self.buffer) + "\n") is not None:
                        return ""
                except (SyntaxError, OverflowError, ValueError):
                    pass  # Let InteractiveConsole report the original Python error.
            return self._pasted.popleft()
        except KeyboardInterrupt:
            self._pasted.clear()
            raise
