"""Non-BMI teaching controls, separate from the raw model surface.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import collections.abc as generic
import logging
import types

import numpy as np

import bmi_explorer.app_logging as app_logging
import bmi_explorer.applicability as applicability
import bmi_explorer.descriptors as descriptors
import bmi_explorer.errors as errors
import bmi_explorer.model as model
import bmi_explorer.reference as reference

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.teaching.controls")


class Explorer:
    """Discover coexisting grids and manage the console's live bmi binding.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param namespace: Console namespace to update when selecting a model.
    :param scenario: Initial built-in fixture name.
    """

    bmi: model.Model
    _namespace: dict[str, object]
    _scenario: str

    def __init__(
        self, namespace: dict[str, object], scenario: str = descriptors.DEFAULT_SCENARIO
    ) -> None:
        """Create and initialize the selected model.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param namespace: Live console locals.
        :param scenario: Initial fixture name.
        :return: None; updates namespace['bmi'].
        :raises BMIExplorerError: If fixture initialization fails.
        """
        self._namespace = namespace
        self._scenario = scenario
        self.use(scenario)

    def list(self) -> generic.Mapping[int, str]:
        """Return the current model's grid inventory without replacing it.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Read-only grid-ID/description mapping, including variables and ranks.
        :raises BMIExplorerError: If the model is not live.
        """
        names: tuple[str, ...] = (
            self.bmi.get_output_var_names() + self.bmi.get_input_var_names()
        )
        grid_ids: tuple[int, ...] = tuple(
            dict.fromkeys(self.bmi.get_var_grid(name) for name in names)
        )
        return types.MappingProxyType({grid: self.describe(grid) for grid in grid_ids})

    def use(self, scenario: str) -> None:
        """Compatibility selector for a fresh all_grids model.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param scenario: Only 'all_grids' is supported.
        :return: None; rebinds bmi in the console; old pointers are detached.
        :raises BMIExplorerError: If the name is unknown; old model stays unchanged.
        """
        replacement: model.Model = model.Model()
        replacement.initialize(scenario)
        if hasattr(self, "bmi"):
            try:
                self.bmi.finalize()
            except errors.BMILifecycleError:
                pass  # An already finalized model can still be reset.
        self.bmi = replacement
        self._scenario = scenario
        self._namespace["bmi"] = replacement

    def reset(self) -> None:
        """Restore the selected scenario using fresh storage.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: None; replaces the model and its console binding.
        """
        self.use(self._scenario)

    def describe(self, name_or_grid: str | int) -> str:
        """Describe a method, current variable, or grid.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name_or_grid: Exact method/variable name or integer grid ID.
        :return: Teaching text, including the relevant fixture policy.
        :raises BMIExplorerError: If the variable/grid/lifecycle is invalid.
        """
        if isinstance(name_or_grid, str) and name_or_grid in reference.operations():
            return reference.describe(name_or_grid)
        if type(name_or_grid) is int:
            grid: descriptors.Grid = self.bmi._grid(name_or_grid, "get_grid_type")
            names: tuple[str, ...] = tuple(
                dict.fromkeys(
                    self.bmi.get_output_var_names() + self.bmi.get_input_var_names()
                )
            )
            variables: str = "; ".join(
                self.describe(name)
                for name in names
                if self.bmi.get_var_grid(name) == name_or_grid
            )
            coordinates: str = (
                ", ".join(
                    f"{axis}={len(getattr(grid, axis))}"
                    for axis in ("x", "y", "z")
                    if applicability.supports(grid, "get_grid_" + axis)
                )
                or "unavailable"
            )
            topology: str = (
                f"nodes/edges/faces={grid.node_count}/{len(grid.edge_nodes)//2}/{len(grid.nodes_per_face)}"
                if grid.kind in applicability.TOPOLOGY_TYPES
                else "topology unavailable"
            )
            return (
                f"grid {name_or_grid} ({grid.label}): {self.bmi.get_grid_type(name_or_grid)}, "
                f"rank={self.bmi.get_grid_rank(name_or_grid)}, nodes={self.bmi.get_grid_size(name_or_grid)}; "
                f"shape={grid.shape or 'unavailable'}, coordinate lengths: {coordinates}; {topology}. "
                f"Variables: {variables}"
            )
        return (
            f"{name_or_grid}: grid={self.bmi.get_var_grid(name_or_grid)}, "
            f"location={self.bmi.get_var_location(name_or_grid)}, type={self.bmi.get_var_type(name_or_grid)}, "
            f"bytes={self.bmi.get_var_nbytes(name_or_grid)}; "
            f"count={self.bmi.get_var_nbytes(name_or_grid)//self.bmi.get_var_itemsize(name_or_grid)}, "
            f"dtype={self.bmi._variable(name_or_grid, 'describe').dtype}"
        )

    def methods(self, grid_id: int) -> tuple[str, ...]:
        """List methods applicable to this fixture's grid family.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid_id: Valid grid identifier.
        :return: Deterministic applicable method names.
        :raises BMIExplorerError: If grid/lifecycle is invalid.
        """
        grid: descriptors.Grid = self.bmi._grid(grid_id, "get_grid_type")
        return tuple(
            name
            for name, entry in reference.operations().items()
            if applicability.supports(grid, name)
        )

    def try_call(self, method_name: str, *args: object) -> object:
        """Invoke one reference BMI method and display its result or expected failure.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param method_name: Exact reference BMI method name.
        :param args: Original positional arguments, passed without repair.
        :return: Actual result, or None after a displayed expected error.
        :raises KeyError: If the name is outside the BMI contract.
        """
        if method_name not in reference.operations():
            raise KeyError(
                f"{method_name!r} is outside the BMI standard; try explorer.methods(0)."
            )
        result: object
        try:
            result = getattr(self.bmi, method_name)(*args)
        except (errors.BMIExplorerError, TypeError) as exc:
            print(f"{type(exc).__name__}: {exc}")
            print("The call was not repaired. Use help_bmi for the required contract.")
            return None
        print(repr(result))
        return result

    def example(self, method: str, grid_id: int | None = None) -> str:
        """Return a copyable example without running or mutating the model.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param method: Reference method name.
        :param grid_id: Optional existing grid to use in the example.
        :return: Help text and explicit grid binding, without selecting a model.
        :raises KeyError: If the method is unknown.
        :raises BMIExplorerError: If the grid or lifecycle is invalid.
        """
        text: str = reference.describe(method)
        if grid_id is not None:
            self.bmi.get_grid_type(grid_id)
            variable: str = next(
                name
                for name in self.bmi.get_output_var_names()
                if self.bmi.get_var_grid(name) == grid_id
            )
            text += f"\nFor this grid: n = {variable!r}; g = {grid_id}\n{reference.operations()[method].example}"
        return text

    def compare(self, a: int, b: int) -> str:
        """Compare two grids on this object without changing values or time.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param a: First current grid ID.
        :param b: Second current grid ID.
        :return: Geometry, variable sizes/bytes and method differences.
        :raises BMIExplorerError: If either ID or lifecycle is invalid.
        """
        first: str = self.describe(a)
        second: str = self.describe(b)
        first_methods: set[str] = set(self.methods(a))
        second_methods: set[str] = set(self.methods(b))
        return (
            f"{first}\n{second}\nOnly on grid {a}: {', '.join(sorted(first_methods-second_methods)) or 'none'}"
            f"\nOnly on grid {b}: {', '.join(sorted(second_methods-first_methods)) or 'none'}"
        )

    def topology(self, grid_id: int) -> str:
        """Render face node and edge IDs using cumulative ragged offsets.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param grid_id: Point or unstructured grid ID.
        :return: Counts and each face boundary, or an explicit no-faces description.
        :raises BMIExplorerError: If ID, applicability or lifecycle is invalid.
        """
        count: int = self.bmi.get_grid_face_count(grid_id)
        sizes: np.ndarray = self.bmi.get_grid_nodes_per_face(
            grid_id, np.empty(count, dtype=np.int32)
        )
        nodes: np.ndarray = self.bmi.get_grid_face_nodes(
            grid_id, np.empty(int(sizes.sum()), dtype=np.int32)
        )
        edges: np.ndarray = self.bmi.get_grid_face_edges(
            grid_id, np.empty(nodes.size, dtype=np.int32)
        )
        rows: list[str] = [
            f"grid {grid_id}: nodes={self.bmi.get_grid_node_count(grid_id)}, edges={self.bmi.get_grid_edge_count(grid_id)}, faces={count}"
        ]
        offset: int = 0
        face: int
        size: np.int32
        for face, size in enumerate(sizes):
            rows.append(
                f"face {face}: nodes={nodes[offset:offset+size].tolist()}, edges={edges[offset:offset+size].tolist()}"
            )
            offset += int(size)
        return "\n".join(rows) if count else rows[0] + "; no faces"

    def tour(self, name: str) -> None:
        """Run a short lesson on the current object without replacing or resetting it.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: 'scalar', 'buffers' or 'grids'.
        :return: None; prints valid/invalid probes, leaving model state intact.
        :raises KeyError: If the tour name is unknown.
        """
        if name not in ("scalar", "buffers", "grids"):
            raise KeyError("Available tours: scalar, buffers, grids")
        if name == "grids":
            uniform: int = self.bmi.get_var_grid(descriptors.VALUE_NAME)
            rectilinear: int = self.bmi.get_var_grid("rectilinear_2d__value")
            print(self.compare(uniform, rectilinear))
            print("Valid: uniform spacing has two entries [2., 5.].")
            self.try_call("get_grid_spacing", uniform, np.empty(2, dtype=np.float64))
            print(
                "Invalid: nonuniform rectilinear spacing; expected BMIGridOperationError."
            )
            self.try_call(
                "get_grid_spacing", rectilinear, np.empty(2, dtype=np.float64)
            )
            return
        variable: str = (
            descriptors.SCALAR_NAME if name == "scalar" else descriptors.VALUE_NAME
        )
        values: np.ndarray = self.bmi.get_value_ptr(variable)
        print(
            "Valid: get_value copies into a caller-owned array; expected current values:",
            values,
        )
        self.try_call("get_value", variable, np.empty_like(values))
        if name == "scalar":
            print(
                "Scalar rank=0, size=1, bytes=8: storage exists without spatial axes."
            )
            print(
                "Invalid: scalar spacing is unavailable; expected BMIGridOperationError."
            )
            self.try_call(
                "get_grid_spacing",
                self.bmi.get_var_grid(variable),
                np.empty(0, dtype=np.float64),
            )
        else:
            print(
                "Invalid: a Python list is not a typed buffer; expected BMITypeError."
            )
            self.try_call("set_value", variable, values.tolist())
            print(
                "Pointers alias live storage. set_value writes in place; copied arrays are independent."
            )
        print(
            "Retained arrays can survive finalize in Python; C++ raw pointer lifetime differs."
        )
