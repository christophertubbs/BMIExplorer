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
    tuple(
        descriptors.Variable(
            f"{grid.label}__value",
            (
                (42.0,)
                if grid.rank == 0
                else tuple(float(i) for i in range(grid.node_count))
            ),
            "1",
            grid=grid_id,
        )
        for grid_id, grid in enumerate(GRIDS)
    )
    + (
        descriptors.Variable(
            "unstructured_mixed__edge_value",
            (10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0),
            "1",
            grid=8,
            location="edge",
        ),
        descriptors.Variable(
            "unstructured_mixed__face_value",
            (20.0, 21.0, 22.0),
            "1",
            grid=8,
            location="face",
        ),
    )
    + tuple(
        descriptors.Variable(
            f"scalar__{dtype}",
            (7,),
            "1",
            dtype=dtype,
            primitive=primitive,
            evolving=False,
        )
        for dtype, primitive in PRIMITIVES.items()
    )
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
