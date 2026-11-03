"""Machine-readable operation metadata derived from the pinned BMI ABC.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import collections.abc as generic
import dataclasses
import inspect
import logging
import types
import typing

import bmipy

import bmi_explorer.app_logging as app_logging
import bmi_explorer.descriptors as descriptors
import bmi_explorer.applicability as applicability
import bmi_explorer.fixtures as fixtures

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.reference.catalog")
API_SOURCE: typing.Final[str] = (
    "https://github.com/csdms/bmi-python/blob/master/src/bmipy/bmi.py"
)
GRID_SOURCE: typing.Final[str] = "https://bmi.csdms.io/en/stable/model_grids.html"


@dataclasses.dataclass(frozen=True, slots=True)
class Operation:
    """Reference signature plus grid applicability and buffer rules.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param signature: Python ABC signature.
    :param grids: Applicable implemented grid families.
    :param dtype: Output element dtype or Python return type.
    :param size: Output length rule.
    :param returns: Identity/copy/scalar/None convention.
    :param example: Copyable example with model variable name n and grid ID g.
    :param error: Expected error on unsupported or malformed calls.
    """

    signature: str
    grids: tuple[str, ...]
    dtype: str
    size: str
    returns: str
    example: str
    error: str


def operations() -> generic.Mapping[str, Operation]:
    """Build a read-only catalog from all abstract methods, without a fixed count.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: Read-only method metadata covering every reference abstract method.
    """
    result: dict[str, Operation] = {}
    name: str
    reference: typing.Callable[..., object]
    signature: inspect.Signature
    parameters: tuple[str, ...]
    grids: tuple[str, ...]
    dtype: str
    size: str
    returns: str
    example: str
    error: str
    for name in sorted(bmipy.Bmi.__abstractmethods__):
        reference = getattr(bmipy.Bmi, name)
        signature = inspect.signature(reference)
        parameters = tuple(signature.parameters)[1:]
        grids = applicability.ALL_TYPES
        dtype = str(signature.return_annotation)
        size = "one Python return value"
        returns = "Python scalar/tuple, or None for lifecycle/setters"
        error = "BMILifecycleError if not initialized/finalized; invalid names/IDs: BMIIndexError"
        example = f"bmi.{name}()"
        if parameters == ("name",):
            example = f"bmi.{name}(n)"
        elif parameters == ("grid",):
            example = f"bmi.{name}(g)"
        if name in applicability.GRID_METHODS:
            grids = applicability.GRID_METHODS[name]
            if len(parameters) > 1:
                field: str = name.removeprefix("get_grid_")
                dtype = (
                    "float64"
                    if field in ("spacing", "origin", "x", "y", "z")
                    else "int32"
                )
                size = {
                    "shape": "grid rank",
                    "spacing": "grid rank",
                    "origin": "grid rank",
                    "x": "rectilinear: nx; points/unstructured: node_count; active axes only",
                    "y": "rectilinear: ny; points/unstructured: node_count; rank >= 2",
                    "z": "rectilinear: nz; points/unstructured: node_count; rank >= 3",
                    "edge_nodes": "2 * edge_count",
                    "face_nodes": "sum(nodes_per_face)",
                    "face_edges": "sum(nodes_per_face)",
                    "nodes_per_face": "face_count",
                }[field]
                returns = "same caller destination; zero-length topology allowed"
                error += "; BMIGridOperationError for unsupported family/axis; BMITypeError/BMIBufferError before writes"
                lengths: dict[str, str] = {
                    "shape": "bmi.get_grid_rank(g)",
                    "spacing": "bmi.get_grid_rank(g)",
                    "origin": "bmi.get_grid_rank(g)",
                    "edge_nodes": "2*bmi.get_grid_edge_count(g)",
                    "face_nodes": "int(bmi.get_grid_nodes_per_face(g, np.empty(bmi.get_grid_face_count(g), dtype=np.int32)).sum())",
                    "face_edges": "int(bmi.get_grid_nodes_per_face(g, np.empty(bmi.get_grid_face_count(g), dtype=np.int32)).sum())",
                    "nodes_per_face": "bmi.get_grid_face_count(g)",
                }
                if field in ("x", "y", "z"):
                    axis_index: int = ("x", "y", "z").index(field) + 1
                    length: str = (
                        f"(int(bmi.get_grid_shape(g, np.empty(bmi.get_grid_rank(g), dtype=np.int32))[-{axis_index}]) if bmi.get_grid_type(g) == 'rectilinear' else bmi.get_grid_size(g))"
                    )
                else:
                    length = lengths[field]
                example = f"bmi.{name}(g, np.empty({length}, dtype=np.{dtype}))"
            elif name not in ("get_grid_type", "get_grid_rank", "get_grid_size"):
                error += "; BMIGridOperationError for unsupported family"
        if name in (
            "get_value",
            "get_value_ptr",
            "get_value_at_indices",
            "set_value",
            "set_value_at_indices",
        ):
            dtype = "exact variable dtype; indices int32"
            size = "variable count; indexed calls: len(inds)"
            returns = (
                "same dest for copy getters; live storage for ptr; None for setters"
            )
            example = {
                "get_value": "bmi.get_value(n, np.empty(bmi.get_var_nbytes(n)//bmi.get_var_itemsize(n), dtype=bmi.get_value_ptr(n).dtype))",
                "get_value_ptr": "bmi.get_value_ptr(n)",
                "get_value_at_indices": "bmi.get_value_at_indices(n, np.empty(1, dtype=bmi.get_value_ptr(n).dtype), np.array([0], dtype=np.int32))",
                "set_value": "bmi.set_value(n, bmi.get_value_ptr(n).copy())",
                "set_value_at_indices": "bmi.set_value_at_indices(n, np.array([0], dtype=np.int32), np.array([9], dtype=bmi.get_value_ptr(n).dtype))",
            }[name]
            error += (
                "; BMITypeError/BMIBufferError/BMIIndexError; validation before writes"
            )
        if name == "initialize":
            example = "fresh = type(bmi)(); fresh.initialize('all_grids')"
        elif name == "update_until":
            example = "bmi.update_until(bmi.get_current_time())"
        result[name] = Operation(
            str(signature), grids, dtype, size, returns, example, error
        )
    return types.MappingProxyType(result)


def describe(method: str) -> str:
    """Render reference metadata, distinguishing BMI requirements and fixture policy.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :param method: Exact reference method name.
    :return: Human-readable method help and a copyable sample.
    :raises KeyError: If the method name is unknown.
    """
    entry: Operation = operations()[method]
    candidates: tuple[descriptors.Grid, ...] = tuple(
        grid for grid in fixtures.GRIDS if applicability.supports(grid, method)
    )
    selected: descriptors.Grid = (
        candidates[-1]
        if method in applicability.GRID_METHODS and "unstructured" in entry.grids
        else candidates[0]
    )
    variable: str = f"{selected.label}__value"
    return (
        f"{method}{entry.signature}\n"
        f"BMI REQUIRED: signature/return from {API_SOURCE}\n"
        f"GRID-TYPE APPLICABILITY: {entry.grids}; {GRID_SOURCE}\n"
        f"C++ PARITY: {entry.dtype}; length={entry.size}; {entry.returns}.\n"
        "EXPLORER POLICY: native, flat, exact dtype/count, contiguous ndarray; no coercion.\n"
        f"Setup: n = {variable!r}; g = bmi.get_var_grid(n)\n"
        f"Example: {entry.example}\nExpected errors: {entry.error}\n"
        "Value mistake: bmi.set_value(n, [1.0]) raises BMITypeError; allocate a typed array.\n"
        "C++ counterpart uses named CamelCase BMI methods and typed caller-owned buffers.\n"
        "Detailed per-method lessons and C++ signatures are scheduled for Phase 4."
    )


def matrix() -> str:
    """Render the current single-scenario operation matrix for checked-in documentation.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.

    :return: Markdown table derived from the reference method catalog.
    """
    rows: list[str] = [
        "# Single-scenario method matrix",
        "",
        "Generated by bmi_explorer.reference.matrix(); all nine grids coexist in all_grids. Axis applicability also depends on rank.",
        "",
        "| Method | Applicable fixtures | Output dtype | Length | Return | Expected error |",
        "|---|---|---|---|---|---|",
    ]
    name: str
    entry: Operation
    for name, entry in operations().items():
        rows.append(
            f"| {name} | {', '.join(entry.grids) or 'unavailable'} | {entry.dtype} | {entry.size} | {entry.returns} | {entry.error} |"
        )
    return "\n".join(rows) + "\n"
