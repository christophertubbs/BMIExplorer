"""Grid dispatch with strict caller-owned geometry and connectivity buffers.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import collections.abc as generic
import logging

import numpy as np

import bmi_explorer.app_logging as app_logging
import bmi_explorer.applicability as applicability
import bmi_explorer.descriptors as descriptors
import bmi_explorer.errors as errors
import bmi_explorer.validation as validation

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.geometry.access")


class GridMethods:
    """Shared grid operations; each call resolves its grid on the same model.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.
    """

    _state: str
    _grids: generic.Mapping[int, descriptors.Grid]

    def _require(self) -> None:
        """Require a live initialized model.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: None; validates lifecycle.
        :raises BMILifecycleError: If uninitialized or finalized.
        """
        if self._state != "initialized":
            raise errors.BMILifecycleError(
                f"Model state is {self._state!r}; initialize a new model with initialize('all_grids')."
            )

    def _grid(self, grid: int, method: str) -> descriptors.Grid:
        """Resolve an exact integer grid ID and check operation applicability.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Exact integer identifier from get_var_grid.
        :param method: Calling BMI method name for applicability and diagnostics.
        :return: Immutable descriptor owned by this model.
        :raises BMIIndexError: For unknown or coercible IDs.
        :raises BMIGridOperationError: For unsupported geometry or inactive axes.
        :raises BMILifecycleError: If the model is not live.
        """
        self._require()
        if type(grid) is not int or grid not in self._grids:
            raise errors.BMIIndexError(
                f"{method}(grid={grid!r}) expected a known integer grid ID. Try bmi.get_var_grid('uniform_2d__value')."
            )
        descriptor: descriptors.Grid = self._grids[grid]
        if not applicability.supports(descriptor, method):
            raise errors.BMIGridOperationError(
                f"{method}(grid={grid}) is not supported for {descriptor.kind}, rank={descriptor.rank}: "
                "this grid has no applicable geometry for that operation. Try explorer.methods(grid_id) or explorer.list()."
            )
        return descriptor

    def _geometry(self, grid: int, field: str, dest: np.ndarray) -> np.ndarray:
        """Copy immutable geometry only after complete applicability/buffer checks.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Exact integer grid ID.
        :param field: Descriptor field corresponding to a BMI grid getter.
        :param dest: Preallocated exact dtype, flat, native, contiguous writable array.
        :return: The identical destination, filled with descriptor values.
        :raises BMIExplorerError: If lifecycle, grid, applicability or buffer is invalid; no writes occur.
        """
        method: str = "get_grid_" + field
        descriptor: descriptors.Grid = self._grid(grid, method)
        values: tuple[int | float, ...] = getattr(descriptor, field)
        dtype: np.dtype = np.dtype(
            "float64" if field in ("spacing", "origin", "x", "y", "z") else "int32"
        )
        destination: np.ndarray = validation.buffer(
            dest, dtype, len(values), f"{method}(grid={grid})", writable=True
        )
        destination[:] = values
        return destination

    def get_grid_type(self, grid: int) -> str:
        """Return the grid type from its immutable descriptor.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :return: Grid type; topology counts may be zero.
        :raises BMIExplorerError: If lifecycle, grid or applicability is invalid.
        """
        descriptor: descriptors.Grid = self._grid(grid, "get_grid_type")
        return descriptor.kind

    def get_grid_rank(self, grid: int) -> int:
        """Return the grid rank from its immutable descriptor.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :return: Grid rank; topology counts may be zero.
        :raises BMIExplorerError: If lifecycle, grid or applicability is invalid.
        """
        descriptor: descriptors.Grid = self._grid(grid, "get_grid_rank")
        return descriptor.rank

    def get_grid_size(self, grid: int) -> int:
        """Return the grid size from its immutable descriptor.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :return: Grid size; topology counts may be zero.
        :raises BMIExplorerError: If lifecycle, grid or applicability is invalid.
        """
        descriptor: descriptors.Grid = self._grid(grid, "get_grid_size")
        return descriptor.node_count

    def get_grid_node_count(self, grid: int) -> int:
        """Return the grid node count from its immutable descriptor.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :return: Grid node count; topology counts may be zero.
        :raises BMIExplorerError: If lifecycle, grid or applicability is invalid.
        """
        descriptor: descriptors.Grid = self._grid(grid, "get_grid_node_count")
        return descriptor.node_count

    def get_grid_edge_count(self, grid: int) -> int:
        """Return the grid edge count from its immutable descriptor.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :return: Grid edge count; topology counts may be zero.
        :raises BMIExplorerError: If lifecycle, grid or applicability is invalid.
        """
        descriptor: descriptors.Grid = self._grid(grid, "get_grid_edge_count")
        return len(descriptor.edge_nodes) // 2

    def get_grid_face_count(self, grid: int) -> int:
        """Return the grid face count from its immutable descriptor.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :return: Grid face count; topology counts may be zero.
        :raises BMIExplorerError: If lifecycle, grid or applicability is invalid.
        """
        descriptor: descriptors.Grid = self._grid(grid, "get_grid_face_count")
        return len(descriptor.nodes_per_face)

    def get_grid_shape(self, grid: int, shape: np.ndarray) -> np.ndarray:
        """Copy shape into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param shape: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "shape", shape)

    def get_grid_spacing(self, grid: int, spacing: np.ndarray) -> np.ndarray:
        """Copy spacing into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param spacing: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "spacing", spacing)

    def get_grid_origin(self, grid: int, origin: np.ndarray) -> np.ndarray:
        """Copy origin into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param origin: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "origin", origin)

    def get_grid_x(self, grid: int, x: np.ndarray) -> np.ndarray:
        """Copy x into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param x: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "x", x)

    def get_grid_y(self, grid: int, y: np.ndarray) -> np.ndarray:
        """Copy y into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param y: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "y", y)

    def get_grid_z(self, grid: int, z: np.ndarray) -> np.ndarray:
        """Copy z into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param z: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "z", z)

    def get_grid_edge_nodes(self, grid: int, edge_nodes: np.ndarray) -> np.ndarray:
        """Copy edge nodes into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param edge_nodes: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "edge_nodes", edge_nodes)

    def get_grid_face_edges(self, grid: int, face_edges: np.ndarray) -> np.ndarray:
        """Copy face edges into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param face_edges: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "face_edges", face_edges)

    def get_grid_face_nodes(self, grid: int, face_nodes: np.ndarray) -> np.ndarray:
        """Copy face nodes into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param face_nodes: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "face_nodes", face_nodes)

    def get_grid_nodes_per_face(
        self, grid: int, nodes_per_face: np.ndarray
    ) -> np.ndarray:
        """Copy nodes per face into the caller's exact typed buffer.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid: Integer grid ID returned by get_var_grid.
        :param nodes_per_face: Flat native contiguous writable output of the documented length/dtype.
        :return: The identical filled destination; empty topology is a valid zero-length copy.
        :raises BMIExplorerError: If lifecycle, applicability or buffer validation fails; no writes occur.
        """
        return self._geometry(grid, "nodes_per_face", nodes_per_face)
