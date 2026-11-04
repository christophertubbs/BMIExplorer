"""Geometry outputs obey the same strict typed-memory contract as value outputs.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import logging

import numpy as np
import pytest

import bmi_explorer.app_logging as app_logging
import bmi_explorer.errors as errors
import bmi_explorer.model as model

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.tests.geometry")


@pytest.mark.parametrize(
    "field,dtype", (("shape", "int32"), ("spacing", "float64"), ("origin", "float64"))
)
@pytest.mark.parametrize(
    "problem",
    ("list", "wrong_dtype", "wrong_length", "2d", "strided", "readonly", "byteorder"),
)
def test_invalid_geometry_buffer(field: str, dtype: str, problem: str) -> None:
    """Reject malformed geometry outputs before destination mutation.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param field: Uniform geometry field to retrieve.
    :param dtype: Required native dtype.
    :param problem: Invalid buffer property to exercise.
    :return: None; verifies controlled errors and unchanged destination contents.
    """
    bmi: model.Model = model.Model()
    bmi.initialize("all_grids")
    destination: object = np.full(2, -99, dtype=dtype)
    if problem == "list":
        destination = [-99, -99]
    elif problem == "wrong_dtype":
        destination = np.full(2, -99, dtype="float32")
    elif problem == "wrong_length":
        destination = np.full(3, -99, dtype=dtype)
    elif problem == "2d":
        destination = np.full((1, 2), -99, dtype=dtype)
    elif problem == "strided":
        destination = np.full(4, -99, dtype=dtype)[::2]
    elif problem == "readonly":
        destination.flags.writeable = False
    elif problem == "byteorder":
        destination = np.full(2, -99, dtype=np.dtype(dtype).newbyteorder("S"))
    before: object = destination.copy()
    with pytest.raises(
        (errors.BMITypeError, errors.BMIBufferError), match="get_grid_" + field
    ):
        getattr(bmi, "get_grid_" + field)(
            bmi.get_var_grid("uniform_2d__slope"), destination
        )
    np.testing.assert_array_equal(destination, before)


@pytest.mark.parametrize(
    "method",
    (
        "get_var_grid",
        "get_var_type",
        "get_var_units",
        "get_var_itemsize",
        "get_var_nbytes",
        "get_var_location",
        "get_value_ptr",
    ),
)
@pytest.mark.parametrize("bad_name", ("missing", None, 0, []))
def test_invalid_variable_name(method: str, bad_name: object) -> None:
    """Unknown and incorrectly typed names produce controlled actionable errors.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param method: Variable metadata or pointer operation.
    :param bad_name: Invalid identifier.
    :return: None; validates exact name lookup without coercion.
    """
    bmi: model.Model = model.Model()
    bmi.initialize("all_grids")
    with pytest.raises(errors.BMIIndexError, match=method):
        getattr(bmi, method)(bad_name)


def test_empty_index_calls() -> None:
    """Explicit empty indexed probes are valid no-ops with exact typed buffers.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; verifies zero-length handling without implicit coercion.
    """
    bmi: model.Model = model.Model()
    bmi.initialize("all_grids")
    name: str = bmi.get_output_var_names()[0]
    dest: np.ndarray = np.empty(0, dtype=np.float64)
    inds: np.ndarray = np.empty(0, dtype=np.int32)
    assert bmi.get_value_at_indices(name, dest, inds) is dest
    bmi.set_value_at_indices(name, inds, dest)
    np.testing.assert_array_equal(bmi.get_value_ptr(name), [1.25])


def test_precision_preserved() -> None:
    """Exact float64 precision survives full reads/writes without downcasting.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; checks extreme, adjacent, and signed-zero values bit for bit.
    """
    bmi: model.Model = model.Model()
    bmi.initialize("all_grids")
    name: str = "unstructured_edges__flow_velocity"
    values: np.ndarray = np.array(
        [
            np.nextafter(1.0, 2.0),
            np.finfo(np.float64).tiny,
            np.finfo(np.float64).max,
            -0.0,
        ],
        dtype=np.float64,
    )
    bmi.set_value(name, values)
    output: np.ndarray = np.empty_like(values)
    bmi.get_value(name, output)
    np.testing.assert_array_equal(output.view(np.uint64), values.view(np.uint64))
