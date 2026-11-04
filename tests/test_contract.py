"""Reference-interface, grid applicability, and lifecycle conformance.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import inspect
import logging

import bmipy
import numpy as np
import pytest

import bmi_explorer.app_logging as app_logging
import bmi_explorer.applicability as applicability
import bmi_explorer.descriptors as descriptors
import bmi_explorer.errors as errors
import bmi_explorer.fixtures as fixtures
import bmi_explorer.model as model
import bmi_explorer.reference as reference

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.tests.contract")


def initialized(scenario: str = "all_grids") -> model.Model:
    """Create an independent initialized model.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param scenario: Built-in fixture token.
    :return: New initialized model.
    """
    result: model.Model = model.Model()
    result.initialize(scenario)
    return result


def test_reference_surface() -> None:
    """Verify every ABC signature and metadata entry without hardcoding the count.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; asserts concrete subclass conformance.
    """
    assert not inspect.isabstract(model.Model)
    assert issubclass(model.Model, bmipy.Bmi)
    assert set(reference.operations()) == bmipy.Bmi.__abstractmethods__
    name: str
    for name in bmipy.Bmi.__abstractmethods__:
        assert inspect.signature(getattr(model.Model, name)) == inspect.signature(
            getattr(bmipy.Bmi, name)
        )
        assert "BMI REQUIRED" in reference.describe(name)
        assert "EXPLORER POLICY" in reference.describe(name)


def test_fixture_metadata() -> None:
    """Check every variable's grid, primitive dtype, location and storage size.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; checks immutable descriptors against independent model storage.
    """
    bmi: model.Model = initialized()
    variable: descriptors.Variable
    assert tuple(fixtures.SCENARIOS) == ("all_grids",)
    assert bmi.get_component_name() == "BMI Explorer"
    assert bmi.get_input_item_count() == bmi.get_output_item_count() == 21
    assert bmi.get_input_var_names() == bmi.get_output_var_names()
    for variable in fixtures.VARIABLES:
        assert bmi.get_var_grid(variable.name) == variable.grid
        assert bmi.get_var_location(variable.name) == variable.location
        assert bmi.get_var_type(variable.name) == variable.primitive
        assert bmi.get_var_units(variable.name) == variable.units
        assert bmi.get_var_itemsize(variable.name) == np.dtype(variable.dtype).itemsize
        assert (
            bmi.get_var_nbytes(variable.name)
            == np.dtype(variable.dtype).itemsize * variable.count
        )
        np.testing.assert_array_equal(
            bmi.get_value_ptr(variable.name), variable.initial
        )


@pytest.mark.parametrize("grid_id", range(9))
@pytest.mark.parametrize(
    "method",
    tuple(name for name in reference.operations() if name.startswith("get_grid_")),
)
def test_grid_unavailable_atomicity(grid_id: int, method: str) -> None:
    """Every family/rank-inapplicable method rejects before destination writes.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param grid_id: A grid on the shared model.
    :param method: Grid operation from the reference registry.
    :return: None; verifies applicability errors preserve sentinels and model values.
    """
    bmi: model.Model = initialized()
    if applicability.supports(fixtures.GRIDS[grid_id], method):
        return
    before: dict[str, np.ndarray] = {
        name: bmi.get_value_ptr(name).copy() for name in bmi.get_output_var_names()
    }
    destination: np.ndarray = np.full(17, -99.0)
    args: tuple[object, ...] = (
        (grid_id, destination)
        if len(inspect.signature(getattr(bmi, method)).parameters) > 1
        else (grid_id,)
    )
    with pytest.raises(errors.BMIGridOperationError, match=method):
        getattr(bmi, method)(*args)
    np.testing.assert_array_equal(destination, -99.0)
    name: str
    for name in before:
        np.testing.assert_array_equal(bmi.get_value_ptr(name), before[name])


@pytest.mark.parametrize("method", ("get_grid_type", "get_grid_rank", "get_grid_size"))
@pytest.mark.parametrize("grid", (-1, 9, True, 0.0, "0", None))
def test_invalid_grid(method: str, grid: object) -> None:
    """Reject unknown IDs and Python coercion of grid identifiers.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param method: Grid metadata operation.
    :param grid: Invalid ID or type.
    :return: None; asserts a controlled error.
    """
    with pytest.raises(errors.BMIIndexError):
        getattr(initialized(), method)(grid)


@pytest.mark.parametrize(
    "time", (-1.0, 3601.0, 10801.0, float("nan"), float("inf"), True, "3600")
)
def test_time_errors_atomic(time: object) -> None:
    """Invalid time targets cannot advance time or values.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param time: Unsupported target.
    :return: None; checks state after rejection.
    """
    bmi: model.Model = initialized()
    name: str = bmi.get_output_var_names()[0]
    before: np.ndarray = bmi.get_value_ptr(name).copy()
    with pytest.raises(errors.BMIExplorerError):
        bmi.update_until(time)
    assert bmi.get_current_time() == 0.0
    np.testing.assert_array_equal(bmi.get_value_ptr(name), before)


def test_lifecycle() -> None:
    """Check update, initialization errors, exact targets and end-of-time rejection.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; checks deterministic lifecycle transitions.
    """
    bmi: model.Model = model.Model()
    with pytest.raises(errors.BMILifecycleError):
        bmi.update()
    with pytest.raises(errors.BMIIndexError):
        bmi.initialize("missing")
    bmi.initialize("all_grids")
    with pytest.raises(errors.BMILifecycleError):
        bmi.initialize("scalar")
    name: str = bmi.get_output_var_names()[0]
    pointer: np.ndarray = bmi.get_value_ptr(name)
    initial: np.ndarray = pointer.copy()
    assert bmi.get_start_time() == bmi.get_current_time() == 0.0
    assert bmi.get_time_step() == 3600.0
    assert bmi.get_time_units() == "s"
    assert bmi.get_end_time() == 10800.0
    bmi.update()
    assert bmi.get_current_time() == 3600.0
    np.testing.assert_array_equal(pointer, initial + 0.05)
    with pytest.raises(errors.BMILifecycleError):
        bmi.update_until(0.0)
    bmi.update_until(10800.0)
    np.testing.assert_allclose(pointer, initial + 0.15, rtol=0, atol=1e-14)
    with pytest.raises(errors.BMILifecycleError):
        bmi.update()
    bmi.finalize()
    np.testing.assert_allclose(pointer, initial + 0.15, rtol=0, atol=1e-14)


@pytest.mark.parametrize("method", tuple(sorted(bmipy.Bmi.__abstractmethods__)))
def test_all_methods_fail_after_finalize(method: str) -> None:
    """No BMI operation remains usable after finalization, including metadata.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param method: Reference method name.
    :return: None; asserts lifecycle validation occurs first.
    """
    bmi: model.Model = initialized()
    bmi.finalize()
    arguments: dict[str, object] = {
        "name": "uniform_2d__slope",
        "grid": 0,
        "dest": np.empty(12),
        "src": np.empty(12),
        "inds": np.array([0], dtype=np.int32),
        "time": 0.0,
        "config_file": "scalar",
    }
    parameter: str
    values: list[object] = [
        arguments.get(parameter, np.empty(12))
        for parameter in inspect.signature(getattr(bmi, method)).parameters
    ]
    with pytest.raises(errors.BMILifecycleError):
        getattr(bmi, method)(*values)
