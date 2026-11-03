"""Immutable fixture metadata, separate from mutable model buffers.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import dataclasses
import logging
import math
import typing

import bmi_explorer.app_logging as app_logging

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.domain.descriptors")
GRID_ID: typing.Final[int] = 0
DEFAULT_SCENARIO: typing.Final[str] = "all_grids"
SCALAR_GRID: typing.Final[str] = "scalar"
UNIFORM_GRID: typing.Final[str] = "uniform_rectilinear"
RECTILINEAR_GRID: typing.Final[str] = "rectilinear"
POINTS_GRID: typing.Final[str] = "points"
UNSTRUCTURED_GRID: typing.Final[str] = "unstructured"
VALUE_NAME: typing.Final[str] = "uniform_2d__value"
SCALAR_NAME: typing.Final[str] = "scalar__value"
TIME_STEP: typing.Final[float] = 3600.0
END_TIME: typing.Final[float] = 10800.0


@dataclasses.dataclass(frozen=True, slots=True)
class Grid:
    """Immutable structured axes or explicit node coordinates and connectivity.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param kind: BMI grid-type string.
    :param shape: Node counts, empty for a scalar.
    :param spacing: Constant increments in ij order.
    :param origin: First node coordinates in ij order.
    :param label: Stable teaching label within the single scenario.
    :param rank: Number of physical dimensions, independent of storage layout.
    :param x: X axis for rectilinear grids, otherwise per-node coordinates.
    :param y: Y axis or per-node coordinates; empty for absent axes.
    :param z: Z axis or per-node coordinates; empty for absent axes.
    :param edge_nodes: Flat tail/head node pairs.
    :param face_nodes: Flat counter-clockwise face boundaries.
    :param face_edges: Edge IDs in corresponding face-boundary order.
    :param nodes_per_face: Number of nodes in each face.
    """

    kind: str
    shape: tuple[int, ...]
    spacing: tuple[float, ...]
    origin: tuple[float, ...]
    label: str
    rank: int
    x: tuple[float, ...] = ()
    y: tuple[float, ...] = ()
    z: tuple[float, ...] = ()
    edge_nodes: tuple[int, ...] = ()
    face_nodes: tuple[int, ...] = ()
    face_edges: tuple[int, ...] = ()
    nodes_per_face: tuple[int, ...] = ()

    @property
    def node_count(self) -> int:
        """Return the geometric node count independently of variable storage.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Product of structured axis lengths, or one logical scalar node.
        """
        return len(self.x) if self.x and not self.shape else math.prod(self.shape)


@dataclasses.dataclass(frozen=True, slots=True)
class Variable:
    """Read/write variable description using immutable initial values.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param name: Variable name (scalar label is illustrative, not certified).
    :param initial: Values restored by a new initialized model.
    :param units: Units of primitive values.
    :param grid: Associated grid identifier.
    :param location: Association with grid nodes.
    :param dtype: Fixed-width NumPy dtype spelling.
    :param primitive: Fixture C++ BMI primitive spelling.
    :param readable: Exposure in output names.
    :param writable: Exposure in input names.
    :param evolving: Whether each model timestep adds one to these values.
    """

    name: str
    initial: tuple[int | float, ...]
    units: str
    grid: int = GRID_ID
    location: str = "node"
    dtype: str = "float64"
    primitive: str = "double"
    readable: bool = True
    writable: bool = True
    evolving: bool = True

    @property
    def count(self) -> int:
        """Return the immutable expected value-buffer element count.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Number of declared initial primitive values.
        """
        return len(self.initial)


@dataclasses.dataclass(frozen=True, slots=True)
class Scenario:
    """Complete immutable multi-grid scenario.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param description: Compact teaching legend.
    :param grids: Immutable grid descriptors; tuple index is the stable grid ID.
    :param variables: Immutable exposed variable descriptors.
    """

    description: str
    grids: tuple[Grid, ...]
    variables: tuple[Variable, ...]
