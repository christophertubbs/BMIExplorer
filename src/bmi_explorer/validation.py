"""Strict caller-owned buffer validation; never coerce user inputs.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import logging

import numpy as np

import bmi_explorer.app_logging as app_logging
import bmi_explorer.errors as errors

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.contract.validation")


def buffer(
    value: object,
    dtype: np.dtype,
    size: int | None,
    context: str,
    writable: bool = False,
) -> np.ndarray:
    """Validate a flat native typed ndarray before any writes.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param value: Caller-supplied buffer; no conversion is attempted.
    :param dtype: Exact native dtype required.
    :param size: Exact element count, or None for any flat length.
    :param context: Method and variable/grid for diagnostics.
    :param writable: Whether the destination must permit writes.
    :return: The original validated ndarray.
    :raises BMITypeError: If type, dtype, or byte order is wrong.
    :raises BMIBufferError: If shape, size, contiguity, or writeability is wrong.
    """
    received: str = type(value).__name__
    if isinstance(value, np.ndarray):
        received += f"(shape={value.shape}, dtype={value.dtype}, C={value.flags.c_contiguous}, writable={value.flags.writeable})"
    expected: str = (
        f"flat C-contiguous numpy.ndarray(dtype={dtype}, size={size if size is not None else 'N'})"
    )
    message: str = (
        f"{context} expected {expected}; received {received}. "
        f"C++ parity requires an existing typed buffer. Try np.empty({size if size is not None else 1}, dtype=np.{dtype})."
    )
    if (
        type(value) is not np.ndarray
        or value.dtype != dtype
        or not value.dtype.isnative
    ):
        raise errors.BMITypeError(message)
    if (
        value.ndim != 1
        or not value.flags.c_contiguous
        or (size is not None and value.size != size)
    ):
        raise errors.BMIBufferError(message)
    if writable and not value.flags.writeable:
        raise errors.BMIBufferError(message + " Destination must be writable.")
    return value


def indices(value: object, size: int, context: str) -> np.ndarray:
    """Validate zero-based int32 indices into a variable buffer.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param value: Caller-supplied index buffer.
    :param size: Variable value count, independent of grid node count.
    :param context: Method and variable for errors.
    :return: Original validated index buffer.
    :raises BMITypeError: If index type or dtype is wrong.
    :raises BMIBufferError: If layout is invalid.
    :raises BMIIndexError: If any index is negative or too large.
    """
    result: np.ndarray = buffer(value, np.dtype("int32"), None, context)
    if np.any(result < 0) or np.any(result >= size):
        raise errors.BMIIndexError(
            f"{context} expected 0 <= index < {size}; received {result!r}. Try np.array([0], dtype=np.int32)."
        )
    return result
