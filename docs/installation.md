# Installation and development

Python 3.11+ is declared; the initial validation environment is the supplied
project-local conda prefix, Python 3.15.2, NumPy 2.5.4, bmipy 2.0.1, pytest 9.2.0.
Other Python versions and platforms have not yet been tested.

## Existing project environment

From the checkout, reuse `.conda`; do not replace it or install into conda base:

```sh
conda activate "$PWD/.conda"
python -m pip install -e '.[dev]'
python -m bmi_explorer
bmi-explorer --list
python -m pytest -q
```

Explicit `.conda/bin/python` and `.conda/bin/bmi-explorer` paths work without shell
activation on Linux. Editable installation is mandatory; no PYTHONPATH changes
or execution of files under src/ are needed.

## Fresh conda environment

The environment.yml includes the editable project/development extra. Run from
the checkout:

```sh
conda env create -f environment.yml -p "$PWD/.conda"
conda activate "$PWD/.conda"
python -m bmi_explorer --scenario all_grids
```

Use `mamba env create` in place of conda when available. `-p` selects a prefix;
without it the file's default environment name is `bmi-explorer`, activated with
`conda activate bmi-explorer`. Conda owns Python, NumPy and pip; pip owns the
editable project, bmipy and its transitive dependencies, prompt_toolkit, Pygments,
and pytest. No compiler
or additional native scientific stack is required by the deterministic scenario.
The upstream bmipy wheel also declares black, click and jinja2 dependencies;
these are upstream transitive requirements, not Explorer runtime features.

## uv project environment

This is an alternative to conda, not an implicit way to activate `.conda`:

```sh
uv sync --extra dev
uv run bmi-explorer --list
uv run python -m pytest -q
uv lock
```

uv project mode manages `.venv` and creates `uv.lock`. Conda is currently the
selected workflow; no uv lock has been generated or validated. If adopting uv
project mode, review and commit its generated lock for repeatable resolution.
For intentional pip-compatible use of the supplied conda interpreter:

```sh
uv pip install --python .conda/bin/python -e '.[dev]'
```

Do not mix package managers for an already conda-owned NumPy unless deliberately
updating the environment ownership policy.

## Verify installed execution outside the checkout

Replace CHECKOUT with the absolute checkout path, then run:

```sh
cd /tmp
CHECKOUT/.conda/bin/python -m bmi_explorer --list
CHECKOUT/.conda/bin/bmi-explorer --scenario all_grids --no-banner
CHECKOUT/.conda/bin/python -m pytest -q CHECKOUT/tests
```

The subprocess integration tests also launch both entrypoints with a temporary cwd.

## Updates, reproducibility and cleanup

bmipy is pinned to 2.0.1 so signature checks detect interface drift. NumPy,
setuptools and pytest use minimum versions; prompt_toolkit is constrained to
`>=3.0.48,<4` and Pygments to `>=2.18,<3`; environment.yml is a portable input,
not a fully locked snapshot. Before dependency upgrades, update metadata and
this document, resolve in an isolated environment, and run the entire suite.
For an exact conda deployment, export a reviewed explicit package list and pip
version snapshot; never publish local credential-bearing URLs or machine paths.

Uninstall the editable package with the selected interpreter's
`python -m pip uninstall bmi-explorer`. Remove a disposable conda prefix using
`conda env remove -p /absolute/prefix` after deactivation. Do not remove the
supplied environment during routine development. uv users can remove a disposable
`.venv` after deactivation and recreate with `uv sync`. Local environments and
IDE state are ignored by Git.


## Terminal editing dependencies

Regular installation includes prompt_toolkit and Pygments; no extra is required.
For an existing editable environment after pulling these changes, run
`python -m pip install -e '.[dev]'` (or the uv pip-compatible command above) to
refresh dependencies. Syntax colors follow the terminal's color capabilities.
The input editor keeps only in-memory history, supports bracketed paste, and
uses Python's standard InteractiveConsole for evaluation. Pipes use plain input.
See [console smoke checks](console-smoke.md) for keyboard and help checks.
