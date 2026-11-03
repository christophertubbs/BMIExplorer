"""Strict value and index contracts, memory identity, and failure atomicity.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import logging

import numpy as np
import pytest

import bmi_explorer.app_logging as app_logging
import bmi_explorer.errors as errors
import bmi_explorer.model as model

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.tests.buffers")


def setup_model(scenario: str = "uniform_2d") -> tuple[model.Model, str]:
    """Create the complete model and select a variable by its grid label.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param scenario: Grid label within all_grids, not a scenario selector.
    :return: Model/name pair, independent of every other test.
    """
    bmi: model.Model = model.Model()
    bmi.initialize("all_grids")
    return bmi, f"{scenario}__value"


def invalid_buffers() -> list[object]:
    """Construct representative inputs NumPy would normally coerce or reshape.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: Independent malformed or wrongly typed buffers.
    """
    return [
        list(range(12)),
        tuple(range(12)),
        1.0,
        np.array(1.0),
        np.zeros((3, 4)),
        np.zeros(11),
        np.zeros(13),
        np.zeros(12, dtype=np.float32),
        np.zeros(12, dtype=np.int64),
        np.zeros(12, dtype=object),
        np.zeros(24)[::2],
        np.zeros(12, dtype=np.dtype("float64").newbyteorder("S")),
        memoryview(np.zeros(12)),
    ]


@pytest.mark.parametrize("bad", invalid_buffers())
@pytest.mark.parametrize("method", ("get_value", "set_value"))
def test_invalid_full_buffer(bad: object, method: str) -> None:
    """Invalid full buffers leave both model state and ndarray destinations untouched.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param bad: Invalid caller input.
    :param method: Full read or write method.
    :return: None; checks validation and atomicity.
    """
    bmi: model.Model
    name: str
    bmi, name = setup_model()
    pointer: np.ndarray = bmi.get_value_ptr(name)
    before: np.ndarray = pointer.copy()
    original: np.ndarray | None = bad.copy() if isinstance(bad, np.ndarray) else None
    with pytest.raises((errors.BMITypeError, errors.BMIBufferError), match=method):
        getattr(bmi, method)(name, bad)
    np.testing.assert_array_equal(pointer, before)
    if original is not None:
        np.testing.assert_array_equal(bad, original)


@pytest.mark.parametrize(
    "bad",
    (
        [0],
        (0,),
        slice(0, 1),
        np.array([True]),
        np.array([0], dtype=np.int64),
        np.array([-1], dtype=np.int32),
        np.array([12], dtype=np.int32),
        np.array([[0]], dtype=np.int32),
        np.arange(4, dtype=np.int32)[::2],
    ),
)
@pytest.mark.parametrize("method", ("get_value_at_indices", "set_value_at_indices"))
def test_invalid_indices(bad: object, method: str) -> None:
    """Reject coercible or out-of-range indices before writing model/destination.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param bad: Invalid indices.
    :param method: Indexed getter/setter.
    :return: None; checks exact-index contract and atomicity.
    """
    bmi: model.Model
    name: str
    bmi, name = setup_model()
    before: np.ndarray = bmi.get_value_ptr(name).copy()
    destination: np.ndarray = np.array([-99.0])
    with pytest.raises(errors.BMIExplorerError):
        if method == "get_value_at_indices":
            bmi.get_value_at_indices(name, destination, bad)
        else:
            bmi.set_value_at_indices(name, bad, destination)
    np.testing.assert_array_equal(destination, [-99.0])
    np.testing.assert_array_equal(bmi.get_value_ptr(name), before)


@pytest.mark.parametrize("scenario", ("scalar", "unstructured_edges", "uniform_2d"))
def test_copy_pointer_and_indexed_values(scenario: str) -> None:
    """Copies are independent, pointers stay live, and indexed methods target values.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param scenario: Fixture under test.
    :return: None; verifies all five value methods.
    """
    bmi: model.Model
    name: str
    bmi, name = setup_model(scenario)
    pointer: np.ndarray = bmi.get_value_ptr(name)
    destination: np.ndarray = np.empty_like(pointer)
    assert bmi.get_value(name, destination) is destination
    assert not np.shares_memory(pointer, destination)
    destination[0] = -10.0
    assert pointer[0] != -10.0
    pointer[0] = 15.0
    assert bmi.get_value(name, destination)[0] == 15.0
    source: np.ndarray = np.full_like(pointer, 9.0)
    bmi.set_value(name, source)
    assert bmi.get_value_ptr(name) is pointer
    np.testing.assert_array_equal(pointer, source)
    source[0] = -100.0
    assert pointer[0] == 9.0
    indices: np.ndarray = np.array([pointer.size - 1, 0], dtype=np.int32)
    selected: np.ndarray = np.empty(2, dtype=np.float64)
    assert bmi.get_value_at_indices(name, selected, indices) is selected
    np.testing.assert_array_equal(selected, [9.0, 9.0])
    bmi.set_value_at_indices(name, indices, np.array([21.0, 31.0]))
    assert pointer[0] == 31.0
    with pytest.raises(errors.BMIIndexError):
        bmi.set_value_at_indices(
            name, np.array([pointer.size], dtype=np.int32), np.array([1.0])
        )


def test_overlap_and_duplicates() -> None:
    """Indexed writes stage aliased inputs and repeated indices select last source.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; verifies deterministic alias and duplicate behavior.
    """
    bmi: model.Model
    name: str
    bmi, name = setup_model("unstructured_edges")
    pointer: np.ndarray = bmi.get_value_ptr(name)
    bmi.set_value_at_indices(name, np.array([3, 2, 1, 0], dtype=np.int32), pointer)
    np.testing.assert_array_equal(pointer, [3, 2, 1, 0])
    bmi.set_value_at_indices(
        name, np.array([0, 0], dtype=np.int32), np.array([5.0, 6.0])
    )
    assert pointer[0] == 6.0


def test_writability_and_lengths() -> None:
    """Read-only destinations and mismatched index/source lengths cannot mutate state.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; checks layout errors beyond dtype and bounds.
    """
    bmi: model.Model
    name: str
    bmi, name = setup_model()
    before: np.ndarray = bmi.get_value_ptr(name).copy()
    destination: np.ndarray = np.empty(12)
    destination.flags.writeable = False
    with pytest.raises(errors.BMIBufferError):
        bmi.get_value(name, destination)
    bmi.set_value(name, destination)  # Read-only input is valid typed source memory.
    bmi.set_value(name, before)
    with pytest.raises(errors.BMIBufferError):
        bmi.set_value_at_indices(
            name, np.array([0, 1], dtype=np.int32), np.array([5.0])
        )
    with pytest.raises(errors.BMIBufferError):
        bmi.get_value_at_indices(name, np.empty(2), np.array([0], dtype=np.int32))
    np.testing.assert_array_equal(bmi.get_value_ptr(name), before)
