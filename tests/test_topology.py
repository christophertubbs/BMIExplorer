"""Mixed-mesh boundary, ragged cardinality and zero-topology acceptance checks.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import dataclasses
import logging

import numpy as np
import pytest

import bmi_explorer.app_logging as app_logging
import bmi_explorer.descriptors as descriptors
import bmi_explorer.errors as errors
import bmi_explorer.explorer as teaching
import bmi_explorer.fixtures as fixtures
import bmi_explorer.model as model

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.tests.topology")


def test_mixed_mesh_boundaries_and_locations() -> None:
    """Reconstruct faces from BMI buffers and verify counts, edges and winding.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: None; verifies valid planar topology and location-specific indexed bounds.
    """
    explorer: teaching.Explorer = teaching.Explorer({})
    bmi: model.Model = explorer.bmi
    grid: int = bmi.get_var_grid("unstructured_mixed__depth")
    assert (
        bmi.get_grid_node_count(grid),
        bmi.get_grid_edge_count(grid),
        bmi.get_grid_face_count(grid),
    ) == (6, 8, 3)
    x: np.ndarray = bmi.get_grid_x(grid, np.empty(6))
    y: np.ndarray = bmi.get_grid_y(grid, np.empty(6))
    edge_nodes: np.ndarray = bmi.get_grid_edge_nodes(
        grid, np.empty(16, dtype=np.int32)
    ).reshape(8, 2)
    sizes: np.ndarray = bmi.get_grid_nodes_per_face(grid, np.empty(3, dtype=np.int32))
    face_nodes: np.ndarray = bmi.get_grid_face_nodes(grid, np.empty(11, dtype=np.int32))
    face_edges: np.ndarray = bmi.get_grid_face_edges(grid, np.empty(11, dtype=np.int32))
    np.testing.assert_array_equal(sizes, [4, 4, 3])
    offset: int = 0
    count: np.int32
    index: int
    nodes: np.ndarray
    edges: np.ndarray
    for count in sizes:
        nodes = face_nodes[offset : offset + count]
        edges = face_edges[offset : offset + count]
        assert len(set(nodes)) == count
        assert np.all((nodes >= 0) & (nodes < 6))
        assert np.all((edges >= 0) & (edges < 8))
        for index in range(int(count)):
            assert set(edge_nodes[edges[index]]) == {
                nodes[index],
                nodes[(index + 1) % count],
            }
        assert (
            np.sum(x[nodes] * y[np.roll(nodes, -1)] - x[np.roll(nodes, -1)] * y[nodes])
            > 0
        )
        offset += int(count)
    location: str
    count_values: int
    for location, count_values in (("node", 6), ("edge", 8), ("face", 3)):
        name: str = "unstructured_mixed__" + (
            {"node": "depth", "edge": "flux", "face": "precipitation_rate"}[location]
        )
        assert bmi.get_var_grid(name) == grid and bmi.get_var_location(name) == location
        assert bmi.get_var_nbytes(name) == count_values * 8
        dest: np.ndarray = np.full(1, -99.0)
        bmi.get_value_at_indices(
            name, dest, np.array([count_values - 1], dtype=np.int32)
        )
        with pytest.raises(errors.BMIIndexError):
            bmi.get_value_at_indices(
                name, dest, np.array([count_values], dtype=np.int32)
            )
    assert "face 2: nodes=[0, 1, 5]" in explorer.topology(grid)


@pytest.mark.parametrize(
    "label,expected_edges",
    (("points_2d", 0), ("points_3d", 0), ("unstructured_edges", 3)),
)
def test_empty_topology(label: str, expected_edges: int) -> None:
    """No-face and disconnected point grids expose exact zero counts/empty buffers.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param label: A grid without faces.
    :param expected_edges: Number of edges (zero for points).
    :return: None; verifies zero-length success and malformed-output atomicity.
    """
    explorer: teaching.Explorer = teaching.Explorer({})
    bmi: model.Model = explorer.bmi
    grid: int = bmi.get_var_grid(fixtures.PRIMARY_NAMES[label])
    assert bmi.get_grid_face_count(grid) == 0
    assert bmi.get_grid_edge_count(grid) == expected_edges
    field: str
    for field in ("face_nodes", "face_edges", "nodes_per_face") + (
        () if expected_edges else ("edge_nodes",)
    ):
        dest: np.ndarray = np.empty(0, dtype=np.int32)
        assert getattr(bmi, "get_grid_" + field)(grid, dest) is dest
        wrong: np.ndarray = np.array([-99], dtype=np.int32)
        with pytest.raises(errors.BMIBufferError):
            getattr(bmi, "get_grid_" + field)(grid, wrong)
        np.testing.assert_array_equal(wrong, [-99])
    assert "no faces" in explorer.topology(grid)


@pytest.mark.parametrize(
    "problem", ("node", "edge", "boundary", "length", "winding", "location")
)
def test_fixture_validation(problem: str) -> None:
    """Corrupt fixture connectivity or variable locations fail before initialization.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param problem: Independently corrupted invariant.
    :return: None; verifies the fixture validator rejects each inconsistency.
    """
    scenario: descriptors.Scenario = fixtures.SCENARIOS["all_grids"]
    grid: descriptors.Grid = scenario.grids[8]
    if problem == "node":
        grid = dataclasses.replace(grid, edge_nodes=(99,) + grid.edge_nodes[1:])
    elif problem == "edge":
        grid = dataclasses.replace(grid, face_edges=(99,) + grid.face_edges[1:])
    elif problem == "boundary":
        grid = dataclasses.replace(grid, face_edges=(0,) + grid.face_edges[1:])
    elif problem == "length":
        grid = dataclasses.replace(grid, nodes_per_face=(4, 4, 4))
    elif problem == "winding":
        grid = dataclasses.replace(grid, y=tuple(-v for v in grid.y))
    else:
        scenario = dataclasses.replace(
            scenario,
            variables=(dataclasses.replace(scenario.variables[0], location="face"),)
            + scenario.variables[1:],
        )
    scenario = dataclasses.replace(scenario, grids=scenario.grids[:8] + (grid,))
    with pytest.raises(ValueError):
        fixtures.validate(scenario)
