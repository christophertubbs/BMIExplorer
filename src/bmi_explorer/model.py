"""Concrete reference BMI implementation with model-owned primitive storage.

TODO(AI-GENERATED): Review and rewrite or approve this implementation.
TODO: AI-generated implementation; human review and rewrite required.
"""

import ctypes
import math
import logging
import types
import collections.abc as generic

import bmipy

import numpy as np

import bmi_explorer.app_logging as app_logging
import bmi_explorer.descriptors as descriptors
import bmi_explorer.errors as errors
import bmi_explorer.validation as validation

LOGGER: logging.Logger = app_logging.get_logger("bmi_explorer.model.lifecycle")

import bmi_explorer.fixtures as fixtures
import bmi_explorer.grids as grids


class Model(grids.GridMethods, bmipy.Bmi):
    """Stateful strict teaching model, initially uninitialized.

    Not thread-safe; callers own synchronization. Previously returned Python
    arrays may survive finalize, but no longer represent a live model.

    TODO(AI-GENERATED): Review and rewrite or approve this implementation.
    TODO: AI-generated implementation; human review and rewrite required.
    """

    _values: dict[str, np.ndarray]
    _time: float
    _variables: generic.Mapping[str, descriptors.Variable]
    _grids: generic.Mapping[int, descriptors.Grid]
    _scenario: descriptors.Scenario

    def __init__(self) -> None:
        """Create an uninitialized model without allocating fixture values.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: None; applies the requested operation.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._state = "new"
        self._values = {}
        self._variables = types.MappingProxyType({})
        self._grids = types.MappingProxyType({})
        self._time = 0.0

    def initialize(self, config_file: str) -> None:
        """Initialize once from a documented built-in scenario token.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param config_file: 'all_grids' or an empty string selecting the same default.
        :return: None; applies the requested operation.
        :raises BMIExplorerError: If lifecycle, token, or platform ABI is invalid.
        """
        if self._state != "new":
            raise errors.BMILifecycleError(
                f"initialize({config_file!r}) requires a new model; current state={self._state!r}. Try explorer.reset()."
            )
        if isinstance(config_file, str) and config_file == "":
            config_file = descriptors.DEFAULT_SCENARIO
        if not isinstance(config_file, str) or config_file not in fixtures.SCENARIOS:
            raise errors.BMIIndexError(
                f"initialize({config_file!r}) expected a built-in scenario token: {tuple(fixtures.SCENARIOS)}. Try initialize('all_grids')."
            )
        abi_types: dict[str, type] = {
            "int8": ctypes.c_byte,
            "uint8": ctypes.c_ubyte,
            "int16": ctypes.c_short,
            "uint16": ctypes.c_ushort,
            "int32": ctypes.c_int,
            "uint32": ctypes.c_uint,
            "int64": ctypes.c_longlong,
            "uint64": ctypes.c_ulonglong,
            "float32": ctypes.c_float,
            "float64": ctypes.c_double,
        }
        if any(
            ctypes.sizeof(c_type) != np.dtype(dtype).itemsize
            for dtype, c_type in abi_types.items()
        ):
            raise errors.BMITypeError(
                "Explorer requires 8/16/32/64-bit C integer and 32/64-bit float teaching types, including 32-bit C int; this platform is unsupported."
            )
        scenario: descriptors.Scenario = fixtures.SCENARIOS[config_file]
        fixtures.validate(scenario)
        variables: dict[str, descriptors.Variable] = {
            item.name: item for item in scenario.variables
        }
        values: dict[str, np.ndarray] = {
            name: np.array(item.initial, dtype=item.dtype)
            for name, item in variables.items()
        }
        self._scenario = scenario
        self._variables = types.MappingProxyType(variables)
        self._grids = types.MappingProxyType(dict(enumerate(scenario.grids)))
        self._values = values
        self._time = 0.0
        self._state = "initialized"
        LOGGER.debug("Initialized scenario %s", config_file)

    def finalize(self) -> None:
        """Invalidate all BMI operations and release model-owned references.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: None; applies the requested operation.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        self._values.clear()
        self._state = "finalized"

    def _variable(self, name: str, method: str) -> descriptors.Variable:
        """Return a known immutable variable descriptor.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact variable name.
        :param method: Calling method for diagnostics.
        :return: Return a known immutable variable descriptor.
        :raises BMIIndexError: If the variable name is unknown.
        """
        self._require()
        if not isinstance(name, str) or name not in self._values:
            raise errors.BMIIndexError(
                f"{method}({name!r}) expected an exposed variable name. Try bmi.get_output_var_names()."
            )
        return self._variables[name]

    def get_component_name(self) -> str:
        """Return the component name.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return the component name.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return "BMI Explorer"

    def get_input_item_count(self) -> int:
        """Return writable variable count.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return writable variable count.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return len(self.get_input_var_names())

    def get_output_item_count(self) -> int:
        """Return readable variable count.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return readable variable count.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return len(self.get_output_var_names())

    def get_input_var_names(self) -> tuple[str]:
        """Return deterministic writable variable names.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return deterministic writable variable names.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return tuple(name for name, item in self._variables.items() if item.writable)

    def get_output_var_names(self) -> tuple[str]:
        """Return deterministic readable variable names.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return deterministic readable variable names.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return tuple(name for name, item in self._variables.items() if item.readable)

    def get_start_time(self) -> float:
        """Return start time in seconds.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return start time in seconds.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return 0.0

    def get_current_time(self) -> float:
        """Return current time in seconds.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return current time in seconds.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return self._time

    def get_end_time(self) -> float:
        """Return final allowed time in seconds.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return final allowed time in seconds.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return descriptors.END_TIME

    def get_time_step(self) -> float:
        """Return the fixed timestep in seconds.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return the fixed timestep in seconds.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return descriptors.TIME_STEP

    def get_time_units(self) -> str:
        """Return the time units label.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: Return the time units label.
        :raises BMILifecycleError: If the model is not initialized.
        """
        self._require()
        return "s"

    def get_var_grid(self, name: str) -> int:
        """Return the variable grid identifier.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact exposed variable name.
        :return: Return the variable grid identifier.
        :raises BMIExplorerError: If the lifecycle or variable name is invalid.
        """
        descriptor: descriptors.Variable = self._variable(name, "get_var_grid")
        return descriptor.grid

    def get_var_location(self, name: str) -> str:
        """Return the variable's node, edge or face association.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact exposed variable name.
        :return: The declared node, edge or face association.
        :raises BMIExplorerError: If the lifecycle or variable name is invalid.
        """
        descriptor: descriptors.Variable = self._variable(name, "get_var_location")
        return descriptor.location

    def get_var_type(self, name: str) -> str:
        """Return the fixture primitive type label.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact exposed variable name.
        :return: Return the fixture primitive type label.
        :raises BMIExplorerError: If the lifecycle or variable name is invalid.
        """
        descriptor: descriptors.Variable = self._variable(name, "get_var_type")
        return descriptor.primitive

    def get_var_units(self, name: str) -> str:
        """Return variable units.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact exposed variable name.
        :return: Return variable units.
        :raises BMIExplorerError: If the lifecycle or variable name is invalid.
        """
        descriptor: descriptors.Variable = self._variable(name, "get_var_units")
        return descriptor.units

    def get_var_itemsize(self, name: str) -> int:
        """Return primitive byte width.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact exposed variable name.
        :return: Return primitive byte width.
        :raises BMIExplorerError: If the lifecycle or variable name is invalid.
        """
        descriptor: descriptors.Variable = self._variable(name, "get_var_itemsize")
        return self._values[name].itemsize

    def get_var_nbytes(self, name: str) -> int:
        """Return actual exposed storage byte count.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact exposed variable name.
        :return: Return actual exposed storage byte count.
        :raises BMIExplorerError: If the lifecycle or variable name is invalid.
        """
        descriptor: descriptors.Variable = self._variable(name, "get_var_nbytes")
        return self._values[name].nbytes

    def get_value_ptr(self, name: str) -> np.ndarray:
        """Return live writable model storage; do not assume validity after finalize.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact variable name.
        :return: Return live writable model storage; do not assume validity after finalize.
        :raises BMIExplorerError: If lifecycle or variable name is invalid.
        """
        self._variable(name, "get_value_ptr")
        return self._values[name]

    def get_value(self, name: str, dest: np.ndarray) -> np.ndarray:
        """Copy into and return the identical caller destination.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact variable name.
        :param dest: Preallocated flat native array with exact dtype and size.
        :return: Copy into and return the identical caller destination.
        :raises BMIExplorerError: If name, lifecycle, or buffer validation fails; no writes occur.
        """
        self._variable(name, "get_value")
        values: np.ndarray = self._values[name]
        destination: np.ndarray = validation.buffer(
            dest, values.dtype, values.size, f"get_value({name!r})", writable=True
        )
        destination[:] = values.copy()
        return destination

    def set_value(self, name: str, src: np.ndarray) -> None:
        """Copy source values in place, preserving existing pointer identity.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact variable name.
        :param src: Exact typed flat source buffer; never broadcast or coerce.
        :return: None; applies the requested operation.
        :raises BMIExplorerError: If validation fails; model storage remains unchanged.
        """
        self._variable(name, "set_value")
        values: np.ndarray = self._values[name]
        source: np.ndarray = validation.buffer(
            src, values.dtype, values.size, f"set_value({name!r})"
        )
        values[:] = source.copy()

    def get_value_at_indices(
        self, name: str, dest: np.ndarray, inds: np.ndarray
    ) -> np.ndarray:
        """Copy one value per flat int32 index and return the caller destination.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact variable name.
        :param dest: Typed flat destination with one entry per index.
        :param inds: Flat C-contiguous int32 indices into the variable values.
        :return: Copy one value per flat int32 index and return the caller destination.
        :raises BMIExplorerError: If validation fails; no destination writes occur.
        """
        self._variable(name, "get_value_at_indices")
        values: np.ndarray = self._values[name]
        context: str = f"get_value_at_indices({name!r})"
        selected: np.ndarray = validation.indices(inds, values.size, context)
        destination: np.ndarray = validation.buffer(
            dest, values.dtype, selected.size, context, writable=True
        )
        destination[:] = values[selected].copy()
        return destination

    def set_value_at_indices(
        self, name: str, inds: np.ndarray, src: np.ndarray
    ) -> None:
        """Set indexed values with staged input; repeated indices use the last source.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param name: Exact variable name.
        :param inds: Flat C-contiguous int32 indices; repeats are allowed by fixture policy.
        :param src: Typed flat source with one value per index.
        :return: None; applies the requested operation.
        :raises BMIExplorerError: If validation fails; storage remains unchanged.
        """
        self._variable(name, "set_value_at_indices")
        values: np.ndarray = self._values[name]
        context: str = f"set_value_at_indices({name!r})"
        selected: np.ndarray = validation.indices(inds, values.size, context)
        source: np.ndarray = validation.buffer(
            src, values.dtype, selected.size, context
        )
        staged_indices: np.ndarray = selected.copy()
        staged_source: np.ndarray = source.copy()
        position: int
        index: np.int32
        for position, index in enumerate(staged_indices):
            values[index] = staged_source[position]

    def update(self) -> None:
        """Advance one timestep using each variable's documented change.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :return: None; applies the requested operation.
        :raises BMIExplorerError: If uninitialized/finalized or already at end time.
        """
        self._require()
        self.update_until(self._time + descriptors.TIME_STEP)

    def update_until(self, time: float) -> None:
        """Advance to a finite integral timestep within the fixture interval.

        TODO(AI-GENERATED): Review and rewrite or approve this implementation.
        TODO: AI-generated implementation; human review and rewrite required.

        :param time: Absolute target seconds; fractional timesteps are an Explorer limitation.
        :return: None; applies the requested operation.
        :raises BMIExplorerError: If target or lifecycle is invalid; state is unchanged.
        """
        self._require()
        if (
            isinstance(time, bool)
            or not isinstance(time, (int, float))
            or not math.isfinite(time)
        ):
            raise errors.BMITypeError(
                f"update_until({time!r}) requires a finite real time. Try update_until(3600.0)."
            )
        if (
            time < self._time
            or time > descriptors.END_TIME
            or time % descriptors.TIME_STEP != 0
        ):
            raise errors.BMILifecycleError(
                f"update_until({time!r}) requires current <= time <= {descriptors.END_TIME} and a multiple of {descriptors.TIME_STEP}. Current={self._time}; try update()."
            )
        steps: int = int((time - self._time) / descriptors.TIME_STEP)
        name: str
        values: np.ndarray
        for name, values in self._values.items():
            if self._variables[name].evolving:
                values[:] += steps * self._variables[name].step_change
        self._time = float(time)
