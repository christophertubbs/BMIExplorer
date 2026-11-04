"""One deterministic scenario with immutable grids and initial value descriptors.

Coordinates and mixed-mesh numbering are Explorer examples, not copied datasets.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import collections.abc as generic
import logging
import types
import typing

import numpy as np

import bmi_explorer.app_logging as app_logging
import bmi_explorer.descriptors as descriptors

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.domain.fixtures")
GRIDS: typing.Final[tuple[descriptors.Grid, ...]] = (
    descriptors.Grid(descriptors.SCALAR_GRID, (), (), (), "scalar", 0),
    descriptors.Grid(
        descriptors.UNIFORM_GRID, (3, 4), (2.0, 5.0), (10.0, 100.0), "uniform_2d", 2
    ),
    descriptors.Grid(
        descriptors.UNIFORM_GRID,
        (2, 3, 4),
        (7.0, 2.0, 5.0),
        (0.0, 10.0, 100.0),
        "uniform_3d",
        3,
    ),
    descriptors.Grid(
        descriptors.RECTILINEAR_GRID,
        (3, 4),
        (),
        (),
        "rectilinear_2d",
        2,
        x=(100.0, 102.0, 107.0, 115.0),
        y=(10.0, 11.0, 14.0),
    ),
    descriptors.Grid(
        descriptors.RECTILINEAR_GRID,
        (2, 3, 4),
        (),
        (),
        "rectilinear_3d",
        3,
        x=(100.0, 102.0, 107.0, 115.0),
        y=(10.0, 11.0, 14.0),
        z=(0.0, 7.0),
    ),
    descriptors.Grid(
        descriptors.POINTS_GRID,
        (),
        (),
        (),
        "points_2d",
        2,
        x=(0.0, 2.0, 3.0, 1.0, -1.0, 1.0),
        y=(0.0, 0.0, 2.0, 3.0, 2.0, 1.0),
    ),
    descriptors.Grid(
        descriptors.POINTS_GRID,
        (),
        (),
        (),
        "points_3d",
        3,
        x=(0.0, 2.0, 3.0, 1.0, -1.0, 1.0),
        y=(0.0, 0.0, 2.0, 3.0, 2.0, 1.0),
        z=(0.0, 1.0, 4.0, 2.0, 5.0, 3.0),
    ),
    descriptors.Grid(
        descriptors.UNSTRUCTURED_GRID,
        (),
        (),
        (),
        "unstructured_edges",
        1,
        x=(0.0, 2.0, 5.0, 9.0),
        edge_nodes=(0, 1, 1, 2, 2, 3),
    ),
    descriptors.Grid(
        descriptors.UNSTRUCTURED_GRID,
        (),
        (),
        (),
        "unstructured_mixed",
        2,
        x=(0.0, 2.0, 3.0, 1.0, -1.0, 1.0),
        y=(0.0, 0.0, 2.0, 3.0, 2.0, 1.0),
        edge_nodes=(0, 1, 1, 2, 2, 3, 3, 4, 4, 0, 1, 5, 3, 5, 0, 5),
        face_nodes=(1, 2, 3, 5, 3, 4, 0, 5, 0, 1, 5),
        face_edges=(1, 2, 6, 5, 3, 4, 7, 6, 0, 5, 7),
        nodes_per_face=(4, 4, 3),
    ),
)
PRIMITIVES: typing.Final[generic.Mapping[str, str]] = types.MappingProxyType(
    {
        "int8": "signed char",
        "uint8": "unsigned char",
        "int16": "short",
        "uint16": "unsigned short",
        "int32": "int",
        "uint32": "unsigned int",
        "int64": "long long",
        "uint64": "unsigned long long",
        "float32": "float",
        "float64": "double",
    }
)
VARIABLES: typing.Final[tuple[descriptors.Variable, ...]] = (
    descriptors.Variable(
        "scalar__velocity",
        (1.25,),
        "m s-1",
        grid=0,
        evolving=True,
        step_change=0.05,
    ),
    descriptors.Variable(
        "uniform_2d__slope",
        (
            0.0124,
            0.0059,
            0.0186,
            0.0116,
            0.0174,
            0.005,
            0.0113,
            0.0177,
            0.0138,
            0.0189,
            0.0036,
            0.0042,
        ),
        "1",
        grid=1,
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "uniform_3d__soil_temp",
        (
            14.2,
            14.0,
            13.8,
            13.5,
            14.5,
            14.3,
            14.1,
            13.9,
            14.8,
            14.6,
            14.4,
            14.2,
            12.6,
            12.5,
            12.4,
            12.2,
            12.8,
            12.7,
            12.6,
            12.4,
            13.0,
            12.9,
            12.8,
            12.6,
        ),
        "degC",
        grid=2,
        evolving=True,
        step_change=0.1,
    ),
    descriptors.Variable(
        "rectilinear_2d__precip_rate",
        (1.2, 1.6, 2.1, 2.4, 1.5, 2.0, 2.8, 3.2, 1.8, 2.5, 3.5, 4.0),
        "mm h-1",
        grid=3,
        evolving=True,
        step_change=0.25,
    ),
    descriptors.Variable(
        "rectilinear_3d__saturation",
        (
            0.45,
            0.48,
            0.52,
            0.55,
            0.5,
            0.54,
            0.58,
            0.6,
            0.55,
            0.59,
            0.62,
            0.65,
            0.65,
            0.68,
            0.72,
            0.75,
            0.7,
            0.74,
            0.78,
            0.8,
            0.75,
            0.79,
            0.82,
            0.85,
        ),
        "1",
        grid=4,
        evolving=True,
        step_change=0.01,
    ),
    descriptors.Variable(
        "points_2d__snow_depth",
        (0.1, 0.3, 0.2, 0.2, 0.32, 0.11),
        "m",
        grid=5,
        evolving=True,
        step_change=-0.002,
    ),
    descriptors.Variable(
        "points_3d__water_level",
        (4.42, 1.882, 1.23, 3.212, 0.846, 2.763),
        "m",
        grid=6,
        evolving=True,
        step_change=0.02,
    ),
    descriptors.Variable(
        "unstructured_edges__flow_velocity",
        (2.1, 1.894, 1.773, 2.435),
        "m s-1",
        grid=7,
        evolving=True,
        step_change=0.05,
    ),
    descriptors.Variable(
        "unstructured_mixed__depth",
        (4.976, 1.597, 1.238, 3.327, 1.942, 3.793),
        "m",
        grid=8,
        evolving=True,
        step_change=0.01,
    ),
    descriptors.Variable(
        "unstructured_mixed__flux",
        (0.436, 0.867, -0.119, 0.232, 1.351, 1.295, 0.787, 0.501),
        "m3 s-1",
        grid=8,
        location="edge",
        evolving=True,
        step_change=0.02,
    ),
    descriptors.Variable(
        "unstructured_mixed__precipitation_rate",
        (2.0, 2.5, 3.0),
        "mm h-1",
        grid=8,
        location="face",
        evolving=True,
        step_change=0.25,
    ),
    descriptors.Variable(
        "scalar__anomaly_class",
        (-3,),
        "1",
        grid=0,
        dtype="int8",
        primitive="signed char",
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "scalar__qc_code",
        (2,),
        "1",
        grid=0,
        dtype="uint8",
        primitive="unsigned char",
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "scalar__scaled_temp",
        (2345,),
        "0.01 degC",
        grid=0,
        dtype="int16",
        primitive="short",
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "scalar__stream_order",
        (5,),
        "1",
        grid=0,
        dtype="uint16",
        primitive="unsigned short",
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "scalar__flow_direction_code",
        (64,),
        "1",
        grid=0,
        dtype="int32",
        primitive="int",
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "scalar__contributing_cells",
        (384,),
        "1",
        grid=0,
        dtype="uint32",
        primitive="unsigned int",
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "scalar__storage_capacity",
        (7030259239,),
        "m3",
        grid=0,
        dtype="int64",
        primitive="long long",
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "scalar__processed_cells",
        (83939242345,),
        "1",
        grid=0,
        dtype="uint64",
        primitive="unsigned long long",
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "scalar__area_sqkm",
        (253.25,),
        "km2",
        grid=0,
        dtype="float32",
        primitive="float",
        evolving=False,
        step_change=0.0,
    ),
    descriptors.Variable(
        "scalar__manning_roughness",
        (0.035,),
        "s m-1/3",
        grid=0,
        evolving=False,
        step_change=0.0,
    ),
)
PRIMARY_NAMES: typing.Final[generic.Mapping[str, str]] = types.MappingProxyType(
    {
        grid.label: variable.name
        for grid, variable in zip(GRIDS, VARIABLES[: len(GRIDS)], strict=True)
    }
)
SAMPLE_NAMES: typing.Final[generic.Mapping[str, str]] = types.MappingProxyType(
    {variable.dtype: variable.name for variable in VARIABLES[-len(PRIMITIVES) :]}
)
SCENARIOS: typing.Final[generic.Mapping[str, descriptors.Scenario]] = (
    types.MappingProxyType(
        {
            descriptors.DEFAULT_SCENARIO: descriptors.Scenario(
                "Nine coexisting grids: scalar; uniform/rectilinear/points ranks 2 and 3; unstructured ranks 1 and 2.",
                GRIDS,
                VARIABLES,
            )
        }
    )
)


def validate(scenario: descriptors.Scenario) -> None:
    """Reject inconsistent fixture descriptors before allocating model state.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param scenario: Complete immutable scenario to validate.
    :return: None; descriptors remain unchanged.
    :raises ValueError: If geometry, connectivity, variable mapping or cardinality is inconsistent.
    """
    grid: descriptors.Grid
    axis: tuple[float, ...]
    axis_index: int
    grid_id: int
    offset: int
    count: int
    nodes: tuple[int, ...]
    edges: tuple[int, ...]
    index: int
    edge: int
    variable: descriptors.Variable
    names: set[str] = set()
    labels: set[str] = set()
    for grid in scenario.grids:
        if grid.label in labels:
            raise ValueError("Grid labels must be unique")
        labels.add(grid.label)
        if grid.rank not in range(4) or grid.node_count < 1:
            raise ValueError(f"Invalid rank/size for {grid.label}")
        if grid.kind == descriptors.SCALAR_GRID:
            if grid.rank != 0 or grid.shape or grid.x or grid.y or grid.z:
                raise ValueError("Scalar must have rank zero and no axes")
        elif grid.shape:
            if len(grid.shape) != grid.rank or any(n < 1 for n in grid.shape):
                raise ValueError(f"Invalid shape for {grid.label}")
        if grid.kind == descriptors.UNIFORM_GRID:
            if (
                len(grid.spacing) != grid.rank
                or len(grid.origin) != grid.rank
                or any(s <= 0 for s in grid.spacing)
            ):
                raise ValueError(f"Invalid uniform geometry for {grid.label}")
        elif grid.kind != descriptors.SCALAR_GRID:
            for axis_index, axis in enumerate((grid.x, grid.y, grid.z)):
                count = (
                    (grid.shape[-1 - axis_index] if grid.shape else grid.node_count)
                    if axis_index < grid.rank
                    else 0
                )
                if len(axis) != count or not all(np.isfinite(v) for v in axis):
                    raise ValueError(f"Invalid axis for {grid.label}")
        if len(grid.edge_nodes) % 2 or any(
            n < 0 or n >= grid.node_count for n in grid.edge_nodes + grid.face_nodes
        ):
            raise ValueError(f"Invalid node IDs for {grid.label}")
        if sum(grid.nodes_per_face) != len(grid.face_nodes) or len(
            grid.face_nodes
        ) != len(grid.face_edges):
            raise ValueError(f"Invalid face lengths for {grid.label}")
        offset = 0
        for count in grid.nodes_per_face:
            if count < 3:
                raise ValueError("A face needs at least three nodes")
            nodes = grid.face_nodes[offset : offset + count]
            edges = grid.face_edges[offset : offset + count]
            for index, edge in enumerate(edges):
                if (
                    edge < 0
                    or 2 * edge >= len(grid.edge_nodes)
                    or set(grid.edge_nodes[2 * edge : 2 * edge + 2])
                    != {nodes[index], nodes[(index + 1) % count]}
                ):
                    raise ValueError(f"Inconsistent face boundary for {grid.label}")
            if (
                grid.rank == 2
                and sum(
                    grid.x[nodes[index]] * grid.y[nodes[(index + 1) % count]]
                    - grid.x[nodes[(index + 1) % count]] * grid.y[nodes[index]]
                    for index in range(count)
                )
                <= 0
            ):
                raise ValueError("Planar faces must have counter-clockwise winding")
            offset += count
    for variable in scenario.variables:
        grid_id = variable.grid
        if variable.name in names or not 0 <= grid_id < len(scenario.grids):
            raise ValueError("Invalid variable name/grid mapping")
        names.add(variable.name)
        grid = scenario.grids[grid_id]
        count = {
            "node": grid.node_count,
            "edge": len(grid.edge_nodes) // 2,
            "face": len(grid.nodes_per_face),
        }.get(variable.location, -1)
        if variable.count != count:
            raise ValueError(f"Invalid value cardinality for {variable.name}")
