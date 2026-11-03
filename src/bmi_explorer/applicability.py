"""Single source of truth for implemented grid-method applicability.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import types
import typing
import collections.abc as generic
import logging

import bmi_explorer.app_logging as app_logging
import bmi_explorer.descriptors as descriptors

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.geometry.applicability")
ALL_TYPES: typing.Final[tuple[str, ...]] = (
    descriptors.SCALAR_GRID,
    descriptors.UNIFORM_GRID,
    descriptors.RECTILINEAR_GRID,
    descriptors.POINTS_GRID,
    descriptors.UNSTRUCTURED_GRID,
)
EXPLICIT_TYPES: typing.Final[tuple[str, ...]] = (
    descriptors.RECTILINEAR_GRID,
    descriptors.POINTS_GRID,
    descriptors.UNSTRUCTURED_GRID,
)
TOPOLOGY_TYPES: typing.Final[tuple[str, ...]] = (
    descriptors.POINTS_GRID,
    descriptors.UNSTRUCTURED_GRID,
)
GRID_METHODS: typing.Final[generic.Mapping[str, tuple[str, ...]]] = (
    types.MappingProxyType(
        {
            "get_grid_type": ALL_TYPES,
            "get_grid_rank": ALL_TYPES,
            "get_grid_size": ALL_TYPES,
            "get_grid_shape": (descriptors.UNIFORM_GRID, descriptors.RECTILINEAR_GRID),
            "get_grid_spacing": (descriptors.UNIFORM_GRID,),
            "get_grid_origin": (descriptors.UNIFORM_GRID,),
            "get_grid_x": EXPLICIT_TYPES,
            "get_grid_y": EXPLICIT_TYPES,
            "get_grid_z": EXPLICIT_TYPES,
            "get_grid_node_count": TOPOLOGY_TYPES,
            "get_grid_edge_count": TOPOLOGY_TYPES,
            "get_grid_face_count": TOPOLOGY_TYPES,
            "get_grid_edge_nodes": TOPOLOGY_TYPES,
            "get_grid_face_nodes": TOPOLOGY_TYPES,
            "get_grid_face_edges": TOPOLOGY_TYPES,
            "get_grid_nodes_per_face": TOPOLOGY_TYPES,
        }
    )
)


def supports(grid: descriptors.Grid, method: str) -> bool:
    """Check family and active axes without executing a BMI operation.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param grid: Immutable geometry descriptor.
    :param method: BMI method name; non-grid methods apply to every grid.
    :return: Whether the method applies to this specific family and rank.
    """
    if grid.kind not in GRID_METHODS.get(method, ALL_TYPES):
        return False
    if method in ("get_grid_x", "get_grid_y", "get_grid_z"):
        return grid.rank >= ("get_grid_x", "get_grid_y", "get_grid_z").index(method) + 1
    return True
