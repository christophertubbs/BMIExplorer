# Python Style Guide

> Install as `STYLE.md` in the repository root. This is the authoritative standard for Python code, packaging, layout, configuration, and developer-facing documentation. `AGENTS.md` governs how an agent performs work; `SPEC.md` governs the required behavior.

## 1. Mandatory principles

- Write maintainable, explicitly typed Python with clear ownership, boundaries, and predictable behavior. Prefer legibility to cleverness.
- **Never use `from __future__ import ...`**, including `annotations`. Set and document a supported Python version in project metadata. Select compatible type annotations accordingly.
- **Import modules/packages, not individual members.** Prefer `import dataclasses`, `import argparse`, `import pathlib`, `import logging`, `import typing`, and `import collections.abc as generic`. Write `@dataclasses.dataclass`, `argparse.ArgumentParser`, `pathlib.Path`, `logging.Logger`, `generic.Mapping`, etc. Do not write `from dataclasses import dataclass`, `from pathlib import Path`, or `from logging import Logger`. Apply the same principle to third-party and local packages. `import package.subpackage.module as alias` is allowed for a meaningful name or collision avoidance; don't disguise member imports as module imports.
- **Use installed, fully qualified package imports.** Prefer `import my_application.configuration` and `import my_application.workflows.execute as execute_workflow`. Avoid relative imports such as `from .whatever import x`, and avoid importing application logic from a working-directory-relative script. Only consider a relative import in a tightly scoped internal package initializer (`__init__.py`) where it is clearly justified. Never depend on the checkout being the current working directory or manipulate `sys.path` to make imports work.
- Annotate parameters, return values, module variables, class attributes, and local variable declarations **even when inference is obvious**. Write `count: int = 0`, `results: list[str] = []`, and `destination: pathlib.Path = ...`. Use `typing.Final` for constants and precise typed collections and protocols. Explicitly annotate `-> None`.
- Every module, class, function, method, private helper, and test helper must be documented. Each callable's docstring **documents every parameter** (including keyword-only parameters and `*args` / `**kwargs` where applicable), **every returned value and its meaning** (including `None`), relevant raised exceptions, and important side effects. Do not substitute type hints for contract documentation. Use consistent Sphinx `:param name:`, `:return:`, and `:raises Exception:` fields. Explain `self`/`cls` through the class/method context rather than repetitive boilerplate.
- Mark AI-authored modules/classes/functions with an explicit `TODO(AI-GENERATED): Review and rewrite or approve this implementation.` in their docstring. Remove the marker only after human review. Do not mark untouched human-authored symbols.
- Avoid repeated magic strings and numeric literals: if the same domain-specific value appears **more than twice**, extract it into a descriptively named constant, enum, or configuration definition. Do not replace standard literals (`0`, `1`, `None`, `True`) mechanically when their meanings are self-evident.

## 2. Small, logical, installed packages

Use a `src/` layout and formal installation as the normal execution model (`uv pip install -e .`, `python -m pip install -e .`, or an equivalent environment-managed installation). Declare build metadata and dependencies in `pyproject.toml`. Test from outside the repository root as well as from the checkout so accidental working-directory imports fail visibly.

Illustrative structure (rename `my_application` for the project):

```text
project/
├── AGENTS.md
├── SPEC.md
├── STYLE.md
├── README.md
├── pyproject.toml
├── uv.lock                      # If uv is selected; commit reproducible locks by policy
├── environment.yml              # If conda is selected
├── .gitignore
├── config/                      # Infrastructure / application configuration
│   ├── log_config.json
│   ├── log_override.example.json
│   └── README.md
├── docs/
│   ├── environment.md           # Every environment variable, type, default, examples
│   ├── installation.md          # uv and conda instructions
│   └── business-configuration.md # Domain/business inputs, schema, examples, precedence
├── src/my_application/
│   ├── __init__.py
│   ├── __main__.py               # Minimal module runner
│   ├── cli.py                    # argparse + dataclass handoff
│   ├── application.py            # Composition and lifecycle
│   ├── app_logging.py            # Logger factory and dictConfig initialization
│   ├── system_configuration.py   # Typed environment adapter
│   ├── constants.py
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── run.py
│   ├── domain/
│   │   └── __init__.py
│   └── infrastructure/
│       └── __init__.py
└── tests/
    ├── test_cli.py
    ├── test_app_logging.py
    └── test_system_configuration.py
```

- Split classes and functions across cohesive modules and subpackages. Do not accumulate enormous multipurpose files. Split by responsibility and dependency direction, not arbitrary line counts; treat ~300–500 lines of mixed logic as a review signal, not permission to make bloated modules smaller only cosmetically.
- Separate entry point, CLI arguments, application orchestration, domain logic, storage, network clients, and environment configuration. Keep `__main__.py` exceptionally small and import the installed package by absolute name.
- Never perform costly initialization, file I/O, or application execution at import time. Library consumers should be able to import the package without running the application.
- Keep optional dependencies confined to relevant features. Avoid creating dependency cycles or deep import chains in `__init__.py`.

## 3. Typed CLI design: argparse + dataclasses

- Use standard `argparse.ArgumentParser` for parsing, help, validation at the CLI boundary, and user-friendly errors. Convert the parsed `argparse.Namespace` into a specifically typed `@dataclasses.dataclass(frozen=True, slots=True)` (where supported) before crossing into application logic.
- Define one explicit dataclass for each meaningful command or argument group. Normalize `str` paths to `pathlib.Path`, constrained choices to enums when useful, and validate dependent arguments at the boundary.
- Keep parser construction, conversion, `main(argv: list[str] | None = None) -> int`, and command dispatch outside the domain services. Never pass `Namespace` through the application. The entry point raises `SystemExit(main())`; the domain layer returns results or raises typed exceptions.
- Use console-script entry points in `pyproject.toml` for installed applications. `python -m my_application` is an alternative invocation, not the only supported deployment mechanism.
- Never infer application resource paths from `pathlib.Path.cwd()` or an assumed source checkout. Use configured absolute locations, user data/config directories, or packaged resources via `importlib.resources` as appropriate.

Example (illustrative; docstrings on actual repository symbols must follow the complete contract rules above):

```python
# my_application/cli.py
import argparse
import dataclasses
import pathlib


@dataclasses.dataclass(frozen=True, slots=True)
class CliOptions:
    """Validated CLI options.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :param input_path: Existing input file selected by the caller.
    :param verbose: Whether verbose diagnostics were requested.
    """

    input_path: pathlib.Path
    verbose: bool


def parse_cli(argv: list[str] | None = None) -> CliOptions:
    """Parse arguments into an independent typed options object.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    :param argv: Arguments to parse, or None to read the process arguments.
    :return: Validated and normalized CLI options.
    :raises SystemExit: If argparse encounters invalid arguments or a help request.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=pathlib.Path)
    parser.add_argument("--verbose", action="store_true")
    parsed: argparse.Namespace = parser.parse_args(argv)
    options: CliOptions = CliOptions(input_path=parsed.input_path, verbose=parsed.verbose)
    return options
```

## 4. Dedicated, identifiable logging

- Every Python file containing execution logic must define a module-level, typed `LOGGER: logging.Logger` using a **central logger factory**. Exempt pure constants, enums, and declarative type-only modules where no behavior is executed. Tests that perform logic should follow an appropriate equivalent or use captured loggers where practical.
- Provide an `app_logging.py` (or similarly distinctive module name), **never a module named `logging.py`**. Centralize logger creation and configuration there.
- **Never use `logging.getLogger(__name__)` as the general convention**: execution as a module can yield `__main__`, and a logger name should communicate meaningful subsystem/role identity that is not merely redundant with `LogRecord.filename`. **No logger may be named `__main__`.** Prefer stable dotted names such as `my_application.ingest.validation` or `my_application.cli.lifecycle`, supplied explicitly to the factory; include instance/component identifiers using the factory or `LoggerAdapter` where relevant, without unbounded cardinality.
- Choose stable, unique logger names by component and purpose, separate from filename. Example: `LOGGER: logging.Logger = my_application.app_logging.get_logger("my_application.ingest.validation")`. The factory can enforce a prefix, validate names, and reject `__main__`.
- For standalone applications, load `config/log_config.json` as the base configuration and initialize with `logging.config.dictConfig`. Then, **after initialization**, optionally load `config/log_override.json` (or an explicit override path) and apply per-logger/package level overrides; for example `urllib3: ERROR`. A missing optional override file must not be an error unless an explicitly supplied path is missing. Validate malformed JSON, logger names, and levels with actionable errors. Do not silently swallow invalid configurations.
- `log_override.json` should be treated as deployment-specific when necessary (ignore it in Git), with a committed `log_override.example.json` showing supported keys, level names, and precedence. Avoid storing secrets in either file.
- Prefer config settings and a documented configuration search order rather than assuming the process was invoked from repository root. For installed packages, locate baseline config through a documented installed resource or deployed config directory. Preserve preexisting loggers where applicable; configure the root logger and `disable_existing_loggers` deliberately.
- The application initializes logging once at its composition/entry boundary, **before applying overrides** and before emitting normal application logs. Library code must not call global `dictConfig` on import or unexpectedly take over host application logging. Library modules may obtain named loggers, but the host owns global setup.
- Use `LOGGER.debug/info/warning/error/exception` with parameterized arguments. Never use `print` for status, progress, diagnostics, warnings, or errors. `print`/stdout is reserved for deliberately interactive content, CLI help, or *machine-consumable program output*; send diagnostics to logging (normally stderr or files) so stdout remains parseable.
- If implementing custom filters/formatters/handlers, preserve thread safety, safe log rotation, predictable error handling, and separation of handler-specific concerns. Treat the referenced logging gist as a design starting point, not a guaranteed bug-free implementation. Explicitly test logging config loading, override ordering, per-package suppression, and logger names.

Reference implementation: https://gist.github.com/christophertubbs/cfdbe7620af722557737c3420c7b4d99

Suggested override format (document and validate it):

```json
{
  "loggers": {
    "urllib3": "ERROR",
    "botocore": "WARNING",
    "my_application.ingest.validation": "DEBUG"
  }
}
```

## 5. Central typed system and environment configuration

- Implement a dedicated `system_configuration.py` (or a focused configuration package) that owns **all application environment reads**, normalization, validation, and typed access. Other application modules should consume a settings object/dataclass or narrow protocol and **avoid `os.environ` / `os.getenv`**. Reusable libraries may read specific documented environment variables where their public contract justifies it, but should prefer caller-supplied configuration.
- Use one app-specific namespace/prefix and named environment keys (`enum.StrEnum` when supported or typed constants) rather than scattering string literals. Provide clearly named typed properties or accessors for `bool`, `int`, `float`, `pathlib.Path`, enums, optional values, and collections as required. Fail clearly for bad inputs; do not use truthiness of an arbitrary nonempty string as a boolean.
- Boolean parsing must be **case-insensitive** after trimming surrounding whitespace. True values: `true`, `t`, `yes`, `y`, `on`, `1`; false values: `false`, `f`, `no`, `n`, `off`, `0`. Anything else raises a clear validation error; a missing key follows the explicitly documented required/default policy.
- Define configuration source precedence explicitly (e.g., CLI > explicit runtime settings > environment > optional `.env` > defaults). Never silently permit `.env` to supersede production environment values. Support deterministic settings overrides for tests without mutating global environment unnecessarily; prefer immutable validated snapshots for application runtime and synchronize shared mutable settings when truly needed.
- Do not derive a root path by walking toward an assumed checkout name. Installed apps must use deployment configuration and installed resources instead. Do not log sensitive values.
- Maintain **`docs/environment.md` outside Python source** listing **every consumed environment variable**, its name, type, allowed values, default, whether required, purpose, precedence, sample invocation before application start, and security considerations. Update the document whenever a key is introduced, renamed, or removed. Explain how to export/unset settings in shell and how to configure them for conda and uv-based runs.
- Test missing, valid, invalid, mixed-case boolean, whitespace, type conversion, and precedence cases.

Reference model: https://gist.github.com/christophertubbs/5a99c1f64163adc552fcfdcbf7e78ea0

## 6. Separate infrastructure configuration from business configuration

- Keep **non-domain application/library configuration** (logging, telemetry, transport defaults, runtime infrastructure settings) together under `config/` or a clearly named installed-resource package. Add `config/README.md` with schema, defaults, and deployment resolution rules.
- Keep **domain/business configuration** in a separate obvious document, such as `docs/business-configuration.md`, and in an explicitly named domain configuration schema/file location. Do not bury domain rules in `log_config.json`, generic infrastructure settings, or implementation constants.
- Define which values are package defaults, administrator deployment settings, environment values, CLI values, and per-job business inputs. Document their precedence and validation separately.
- Check in templates and schemas, but exclude environment-specific secrets, private configuration, and local override files. Resolve config paths independently from `cwd`.

## 7. Dependencies, conda, and uv documentation

- The package is **formally installed** in the executing environment. Declare dependencies and Python-version support in `pyproject.toml`; document extras and optional tooling. Do not use `PYTHONPATH=.` or `python src/my_application/...` as normal operation.
- Maintain `docs/installation.md` with **both conda and uv workflows**, even if only one is the project's preferred environment manager. Include supported Python versions, environment creation, install/editable install, how to run installed CLI commands and tests from outside repository root, dependency update/lock procedure, reproducibility and version pinning, and cleanup.
- For conda: document `environment.yml`, `conda env create -f environment.yml`, `conda activate <name>`, and how the project is installed into that environment; explain the conda/pip ownership boundary where applicable and use conda/mamba for native dependencies when needed.
- For uv: document `uv sync`, `uv run <command>`, `uv lock`, `uv pip install -e .` when applicable, and `uv.lock` commit policy. Distinguish uv-managed project environments from uv's pip-compatible mode. Do not assert uv and conda automatically share the same environment; show an intentional integration if supported.
- Never add dependencies gratuitously or switch an existing project's approved resolver without explicit scope. Record system/native prerequisites for NetCDF, geospatial, or MPI stacks where relevant.

## 8. Exceptions, tests, and readability

- Make failures explicit and actionable. Catch specific exceptions and preserve context (`raise ... from exc`); do not mask errors with broad exception handlers. Resource acquisition must have reliable cleanup (`with`, `contextlib`, or `try/finally`).
- Avoid hidden module-global mutable state. Inject clocks, file systems, clients, and configuration where useful for testing. Document thread/process safety for shared services.
- Tests must validate contracts, error branches, CLI parsing, named logging, logging overrides, typed settings, installed import paths, and package execution outside root. Prefer deterministic fixtures and verify both expected outputs and meaningful side effects.
- Use descriptive names and straightforward conditionals. Preserve public API compatibility unless authorized by `SPEC.md`. Use existing appropriate standard library features before adding new dependencies.

## 9. Review checklist

- [ ] No `__future__` imports; no member-level `from ... import ...` imports; `collections.abc` is imported as `generic`.
- [ ] Installed-package absolute imports; no cwd-dependent imports or source-root execution assumptions.
- [ ] Every declared variable, field, parameter and return is typed; every callable documents **all inputs and return values**, exceptions, and relevant side effects.
- [ ] AI-authored symbols have `TODO(AI-GENERATED)` in docstrings pending review.
- [ ] Cohesive small modules, separate entry point/CLI/business logic, and `argparse` plus dataclasses.
- [ ] Each logic module has an explicit, stable, identifiable logger, never `__main__`.
- [ ] Application logging uses `dictConfig` from `log_config.json`; optional `log_override.json` is applied **after** initialization.
- [ ] Diagnostics and progress use logging, not `print`; stdout remains meaningful to human or script consumers.
- [ ] Typed centralized environment accessor, documented boolean tokens, no scattered application `os.environ` access.
- [ ] `config/` holds infrastructure settings; business configuration has distinct schema/docs.
- [ ] Every environment key is listed in `docs/environment.md`; `docs/installation.md` covers **conda and uv**.
- [ ] Repeated domain-specific literals appearing more than twice are named, without needless abstraction of universal values.
- [ ] Tests cover the important behavior, error cases, and installation model.
