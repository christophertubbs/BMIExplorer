"""Controlled educational exceptions.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""


class BMIExplorerError(Exception):
    """Base class for expected teaching errors.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.
    """


class BMITypeError(BMIExplorerError, TypeError):
    """Invalid argument type; implicit coercion is forbidden.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.
    """


class BMIBufferError(BMIExplorerError, ValueError):
    """Invalid caller-owned array layout or size.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.
    """


class BMIIndexError(BMIExplorerError, IndexError):
    """Unknown variable/grid or out-of-range flat index.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.
    """


class BMIGridOperationError(BMIExplorerError, NotImplementedError):
    """Operation is unavailable for the selected grid.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.
    """


class BMILifecycleError(BMIExplorerError, RuntimeError):
    """Operation is invalid in the current lifecycle state.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.
    """
