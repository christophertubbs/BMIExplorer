"""Independent acceptance examples for all grids coexisting on one BMI object.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import dataclasses
import code
import logging
import typing

import numpy as np
import pytest

import bmi_explorer.app_logging as app_logging
import bmi_explorer.console as console
import bmi_explorer.descriptors as descriptors
import bmi_explorer.errors as errors
import bmi_explorer.explorer as teaching
import bmi_explorer.fixtures as fixtures
import bmi_explorer.model as model
import bmi_explorer.reference as reference

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.tests.scenario")
EXPECTED: typing.Final[tuple[tuple[str, str, int, int], ...]] = (
    ("scalar", "scalar", 0, 1),
    ("uniform_2d", "uniform_rectilinear", 2, 12),
    ("uniform_3d", "uniform_rectilinear", 3, 24),
    ("rectilinear_2d", "rectilinear", 2, 12),
    ("rectilinear_3d", "rectilinear", 3, 24),
    ("points_2d", "points", 2, 6),
    ("points_3d", "points", 3, 6),
    ("unstructured_edges", "unstructured", 1, 4),
    ("unstructured_mixed", "unstructured", 2, 6),
)
GEOMETRY: typing.Final[tuple[tuple[str, str, tuple[int | float, ...]], ...]] = (
    ("uniform_2d", "shape", (3, 4)),
    ("uniform_2d", "spacing", (2.0, 5.0)),
    ("uniform_2d", "origin", (10.0, 100.0)),
    ("uniform_3d", "shape", (2, 3, 4)),
    ("uniform_3d", "spacing", (7.0, 2.0, 5.0)),
    ("uniform_3d", "origin", (0.0, 10.0, 100.0)),
    ("rectilinear_2d", "shape", (3, 4)),
    ("rectilinear_2d", "x", (100.0, 102.0, 107.0, 115.0)),
    ("rectilinear_2d", "y", (10.0, 11.0, 14.0)),
    ("rectilinear_3d", "shape", (2, 3, 4)),
    ("rectilinear_3d", "x", (100.0, 102.0, 107.0, 115.0)),
    ("rectilinear_3d", "y", (10.0, 11.0, 14.0)),
    ("rectilinear_3d", "z", (0.0, 7.0)),
    ("points_2d", "x", (0.0, 2.0, 3.0, 1.0, -1.0, 1.0)),
    ("points_2d", "y", (0.0, 0.0, 2.0, 3.0, 2.0, 1.0)),
    ("points_3d", "x", (0.0, 2.0, 3.0, 1.0, -1.0, 1.0)),
    ("points_3d", "y", (0.0, 0.0, 2.0, 3.0, 2.0, 1.0)),
    ("points_3d", "z", (0.0, 1.0, 4.0, 2.0, 5.0, 3.0)),
    ("unstructured_edges", "x", (0.0, 2.0, 5.0, 9.0)),
    ("unstructured_edges", "edge_nodes", (0, 1, 1, 2, 2, 3)),
    ("unstructured_mixed", "x", (0.0, 2.0, 3.0, 1.0, -1.0, 1.0)),
    ("unstructured_mixed", "y", (0.0, 0.0, 2.0, 3.0, 2.0, 1.0)),
    (
        "unstructured_mixed",
        "edge_nodes",
        (0, 1, 1, 2, 2, 3, 3, 4, 4, 0, 1, 5, 3, 5, 0, 5),
    ),
    ("unstructured_mixed", "nodes_per_face", (4, 4, 3)),
    ("unstructured_mixed", "face_nodes", (1, 2, 3, 5, 3, 4, 0, 5, 0, 1, 5)),
    ("unstructured_mixed", "face_edges", (1, 2, 6, 5, 3, 4, 7, 6, 0, 5, 7)),
)


def initialized() -> model.Model:
    """Build the sole complete scenario with independent state.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: A new initialized model with all nine grids.
    """
    bmi: model.Model = model.Model()
    bmi.initialize("")
    return bmi


def test_inventory_and_shared_state() -> None:
    """Interleave queries and writes across every family without model replacement.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; checks exact ranks/sizes, discovery, isolation and shared time.
    """
    bmi: model.Model = initialized()
    grid_ids: set[int] = {
        bmi.get_var_grid(name)
        for name in bmi.get_input_var_names() + bmi.get_output_var_names()
    }
    assert grid_ids == set(range(9))
    pointers: dict[str, np.ndarray] = {
        name: bmi.get_value_ptr(name) for name in bmi.get_output_var_names()
    }
    before: dict[str, np.ndarray] = {
        name: array.copy() for name, array in pointers.items()
    }
    label: str
    kind: str
    rank: int
    size: int
    grid: int
    name: str
    for label, kind, rank, size in reversed(EXPECTED):
        name = fixtures.PRIMARY_NAMES[label]
        grid = bmi.get_var_grid(name)
        assert (
            bmi.get_grid_type(grid),
            bmi.get_grid_rank(grid),
            bmi.get_grid_size(grid),
        ) == (kind, rank, size)
        assert pointers[name].size == size and pointers[name].dtype == np.float64
    bmi.set_value("uniform_2d__slope", np.full(12, 99.0))
    for name in pointers:
        assert bmi.get_value_ptr(name) is pointers[name]
        np.testing.assert_array_equal(
            pointers[name], 99.0 if name == "uniform_2d__slope" else before[name]
        )
    bmi.update()
    assert bmi.get_current_time() == 3600.0
    for name in pointers:
        assert bmi.get_value_ptr(name) is pointers[name]
        variable: descriptors.Variable = next(
            v for v in fixtures.VARIABLES if v.name == name
        )
        np.testing.assert_allclose(
            pointers[name],
            (99.0 if name == "uniform_2d__slope" else before[name])
            + variable.step_change,
            rtol=0,
            atol=1e-12,
        )


@pytest.mark.parametrize("label,field,expected", GEOMETRY)
def test_exact_geometry(
    label: str, field: str, expected: tuple[int | float, ...]
) -> None:
    """Coordinate and topology results match independently specified numeric arrays.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param label: Grid fixture label.
    :param field: BMI geometry/topology field.
    :param expected: Independent expected values in BMI order.
    :return: None; asserts buffer identity, exact output, and metadata isolation.
    """
    bmi: model.Model = initialized()
    grid: int = bmi.get_var_grid(fixtures.PRIMARY_NAMES[label])
    dtype: str = "float64" if field in ("x", "y", "z", "spacing", "origin") else "int32"
    dest: np.ndarray = np.full(len(expected), -99, dtype=dtype)
    assert getattr(bmi, "get_grid_" + field)(grid, dest) is dest
    np.testing.assert_array_equal(dest, expected)
    dest[:] = -1
    getattr(bmi, "get_grid_" + field)(grid, dest)
    np.testing.assert_array_equal(dest, expected)


@pytest.mark.parametrize("label,field,expected", GEOMETRY)
@pytest.mark.parametrize(
    "problem", ("list", "dtype", "length", "rank", "strided", "readonly", "byteorder")
)
def test_geometry_buffer_failures(
    label: str, field: str, expected: tuple[int | float, ...], problem: str
) -> None:
    """Every applicable geometry and topology getter validates before writing.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param label: Grid label.
    :param field: Applicable getter suffix.
    :param expected: Correct output used to derive buffer length.
    :param problem: Invalid caller-memory property.
    :return: None; verifies errors leave destinations unchanged.
    """
    bmi: model.Model = initialized()
    dtype: str = "float64" if field in ("x", "y", "z", "spacing", "origin") else "int32"
    count: int = len(expected)
    dest: object = np.full(count, -99, dtype=dtype)
    if problem == "list":
        dest = [-99] * count
    elif problem == "dtype":
        dest = np.full(count, -99, dtype="float32")
    elif problem == "length":
        dest = np.full(count + 1, -99, dtype=dtype)
    elif problem == "rank":
        dest = dest.reshape(1, count)
    elif problem == "strided":
        dest = np.full(count * 2, -99, dtype=dtype)[::2]
    elif problem == "readonly":
        dest.flags.writeable = False
    elif problem == "byteorder":
        dest = np.full(count, -99, dtype=np.dtype(dtype).newbyteorder("S"))
    before: object = dest.copy()
    with pytest.raises((errors.BMIBufferError, errors.BMITypeError)):
        getattr(bmi, "get_grid_" + field)(
            bmi.get_var_grid(fixtures.PRIMARY_NAMES[label]), dest
        )
    np.testing.assert_array_equal(dest, before)


def test_reset_comparison_and_tours() -> None:
    """Comparisons/tours preserve the object; reset restores every variable and clock.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; checks compatibility rejection, reset, pointers and immutable metadata.
    """
    session: code.InteractiveConsole = console.create("all_grids")
    explorer: teaching.Explorer = session.locals["explorer"]
    bmi: model.Model = explorer.bmi
    inventory: object = explorer.list()
    pointers: dict[str, np.ndarray] = {
        name: bmi.get_value_ptr(name) for name in bmi.get_output_var_names()
    }
    name: str
    for name in pointers:
        bmi.set_value(name, np.full_like(pointers[name], 9))
    bmi.update()
    before: dict[str, np.ndarray] = {
        name: array.copy() for name, array in pointers.items()
    }
    label: str
    other: str
    for label, other in (
        ("uniform_2d", "uniform_3d"),
        ("rectilinear_2d", "rectilinear_3d"),
        ("points_2d", "points_3d"),
        ("unstructured_edges", "unstructured_mixed"),
        ("uniform_2d", "rectilinear_2d"),
    ):
        result: str = explorer.compare(
            bmi.get_var_grid(fixtures.PRIMARY_NAMES[label]),
            bmi.get_var_grid(fixtures.PRIMARY_NAMES[other]),
        )
        assert label in result and other in result and "bytes=" in result
    assert "get_grid_z" not in explorer.methods(
        bmi.get_var_grid("points_2d__snow_depth")
    )
    assert "get_grid_z" in explorer.methods(bmi.get_var_grid("points_3d__water_level"))
    for name in ("scalar", "buffers", "grids"):
        explorer.tour(name)
    assert explorer.bmi is bmi and session.locals["bmi"] is bmi
    assert bmi.get_current_time() == 3600.0
    for name in before:
        np.testing.assert_array_equal(pointers[name], before[name])
    with pytest.raises(errors.BMIIndexError):
        explorer.use("scalar")
    assert explorer.bmi is bmi
    explorer.reset()
    assert explorer.bmi is not bmi and explorer.bmi.get_current_time() == 0.0
    assert explorer.list() == inventory
    for name in before:
        assert explorer.bmi.get_value_ptr(name) is not pointers[name]
        np.testing.assert_array_equal(pointers[name], before[name])
    with pytest.raises(errors.BMILifecycleError):
        bmi.get_grid_rank(0)
    with pytest.raises(TypeError):
        explorer.list()[0] = "changed"
    with pytest.raises(dataclasses.FrozenInstanceError):
        fixtures.GRIDS[0].rank = 3
    with pytest.raises(TypeError):
        session.locals["scenarios"]["extra"] = fixtures.SCENARIOS["all_grids"]


@pytest.mark.parametrize("dtype", tuple(fixtures.PRIMITIVES))
def test_primitive_extremes(dtype: str) -> None:
    """Typed scalar samples preserve integer boundaries and floating precision.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param dtype: One of all ten fixed-width sample dtypes.
    :return: None; verifies full/indexed copies, pointer identity and wrong-dtype rejection.
    """
    bmi: model.Model = initialized()
    name: str = fixtures.SAMPLE_NAMES[dtype]
    native: np.dtype = np.dtype(dtype)
    values: tuple[int | float, ...] = (
        (np.iinfo(native).min, np.iinfo(native).max)
        if native.kind in "iu"
        else (
            np.finfo(native).tiny,
            np.finfo(native).max,
            -0.0,
            np.nextafter(native.type(1), native.type(2)),
        )
    )
    value: int | float
    pointer: np.ndarray = bmi.get_value_ptr(name)
    indices: np.ndarray = np.array([0], dtype=np.int32)
    for value in values:
        source: np.ndarray = np.array([value], dtype=native)
        dest: np.ndarray = np.empty_like(source)
        bmi.set_value(name, source)
        assert bmi.get_value(name, dest) is dest
        assert dest.tobytes() == source.tobytes()
        bmi.set_value_at_indices(name, indices, source)
        assert bmi.get_value_at_indices(name, dest, indices) is dest
        assert dest.tobytes() == source.tobytes()
        assert bmi.get_value_ptr(name) is pointer
    with pytest.raises(errors.BMITypeError):
        bmi.set_value(
            name, np.array([1], dtype=np.float32 if dtype == "float64" else np.float64)
        )
    np.testing.assert_array_equal(pointer, source)


def test_help_examples_execute() -> None:
    """Every catalog example has valid setup and can execute without changing models.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; runs documented setup/examples on fresh live models.
    """
    method: str
    entry: reference.Operation
    for method, entry in reference.operations().items():
        bmi: model.Model = initialized()
        namespace: dict[str, object] = {"bmi": bmi, "np": np}
        setup: str = reference.describe(method).split("Setup: ", 1)[1].split("\n", 1)[0]
        exec(setup, namespace)
        exec(entry.example, namespace)


@pytest.mark.parametrize(
    "token",
    ("scalar", "uniform_2d", "uniform_1d", "missing", None, [], np.array([1, 2])),
)
def test_reject_legacy_and_invalid_initialization(token: object) -> None:
    """Rejected selectors leave a fresh model available for a valid initialization.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param token: Unsupported legacy selector or incorrectly typed config.
    :return: None; verifies controlled diagnostics and initialization atomicity.
    """
    bmi: model.Model = model.Model()
    with pytest.raises(errors.BMIIndexError):
        bmi.initialize(token)
    bmi.initialize("all_grids")
    assert len({bmi.get_var_grid(name) for name in bmi.get_output_var_names()}) == 9


def test_unsupported_abi(monkeypatch: pytest.MonkeyPatch) -> None:
    """A mismatched C int width fails before model state becomes initialized.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param monkeypatch: Restores the simulated platform ABI after the check.
    :return: None; confirms a usable fresh model remains after the rejection.
    """
    bmi: model.Model = model.Model()
    with monkeypatch.context() as patch:
        patch.setattr(model.ctypes, "c_int", model.ctypes.c_short)
        with pytest.raises(errors.BMITypeError, match="teaching types"):
            bmi.initialize("all_grids")
    bmi.initialize("all_grids")
    assert bmi.get_current_time() == 0.0


def test_three_dimensional_index_order() -> None:
    """Layer/row/column lookup agrees with x-fastest C-order flattened storage.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; independently checks [1,1,2] maps to flat index 18 on both 3D grids.
    """
    bmi: model.Model = initialized()
    label: str
    expected_value: float
    for label, expected_value in (("uniform_3d", 12.6), ("rectilinear_3d", 0.78)):
        name: str = fixtures.PRIMARY_NAMES[label]
        dest: np.ndarray = np.empty(1, dtype=np.float64)
        bmi.get_value_at_indices(name, dest, np.array([18], dtype=np.int32))
        np.testing.assert_array_equal(dest, [expected_value])
        np.testing.assert_array_equal(
            bmi.get_value_ptr(name).reshape(2, 3, 4)[1, 1, 2], expected_value
        )


@pytest.mark.parametrize(
    "name,units,minimum,maximum,change",
    [
        ("scalar__velocity", "m s-1", 0.5, 3.0, 0.05),
        ("uniform_2d__slope", "1", 0.0, 0.05, 0.0),
        ("uniform_3d__soil_temp", "degC", 10.0, 20.0, 0.1),
        ("rectilinear_2d__precip_rate", "mm h-1", 0.0, 10.0, 0.25),
        ("rectilinear_3d__saturation", "1", 0.0, 1.0, 0.01),
        ("points_2d__snow_depth", "m", 0.0, 0.5, -0.002),
        ("points_3d__water_level", "m", 0.0, 6.0, 0.02),
        ("unstructured_edges__flow_velocity", "m s-1", 0.0, 4.0, 0.05),
        ("unstructured_mixed__depth", "m", 0.0, 6.0, 0.01),
        ("unstructured_mixed__flux", "m3 s-1", -2.0, 2.0, 0.02),
        ("unstructured_mixed__precipitation_rate", "mm h-1", 0.0, 10.0, 0.25),
        ("scalar__anomaly_class", "1", -3.0, 3.0, 0.0),
        ("scalar__qc_code", "1", 0.0, 3.0, 0.0),
        ("scalar__scaled_temp", "0.01 degC", 1000.0, 3000.0, 0.0),
        ("scalar__stream_order", "1", 1.0, 8.0, 0.0),
        ("scalar__flow_direction_code", "1", 1.0, 128.0, 0.0),
        ("scalar__contributing_cells", "1", 1.0, 1000.0, 0.0),
        ("scalar__storage_capacity", "m3", 1e9, 1e10, 0.0),
        ("scalar__processed_cells", "1", 1e10, 1e11, 0.0),
        ("scalar__area_sqkm", "km2", 200.0, 300.0, 0.0),
        ("scalar__manning_roughness", "s m-1/3", 0.02, 0.06, 0.0),
    ],
)
def test_hydrological_samples(
    name: str, units: str, minimum: float, maximum: float, change: float
) -> None:
    """Shipped samples and every hourly update stay plausible in documented units.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.

    These are acceptance ranges for this synthetic dataset, not model write limits.

    :param name: Independent expected hydrological variable name.
    :param units: Stored measurement units, including any temperature scale.
    :param minimum: Lower acceptance bound for this sample dataset.
    :param maximum: Upper acceptance bound for this sample dataset.
    :param change: Expected change in stored units per hour; zero for static data.
    :return: None; verifies all timesteps, direct advance, pointer identity and reset.
    """
    session: code.InteractiveConsole = console.create("all_grids")
    explorer: teaching.Explorer = session.locals["explorer"]
    bmi: model.Model = explorer.bmi
    pointer: np.ndarray = bmi.get_value_ptr(name)
    initial: np.ndarray = pointer.copy()
    assert bmi.get_var_units(name) == units
    step: int
    for step in range(4):
        if step:
            bmi.update()
        assert bmi.get_value_ptr(name) is pointer
        assert np.all(np.isfinite(pointer))
        assert np.all((pointer >= minimum) & (pointer <= maximum))
        np.testing.assert_allclose(pointer, initial + step * change, rtol=0, atol=1e-12)
    direct: model.Model = initialized()
    direct.update_until(10800.0)
    np.testing.assert_allclose(direct.get_value_ptr(name), pointer, rtol=0, atol=1e-12)
    explorer.reset()
    np.testing.assert_array_equal(explorer.bmi.get_value_ptr(name), initial)
