/** Concrete browser-local BMI matching the linked BMI-JS method surface.
 * Interface: https://github.com/uihilab/BMI-JS/blob/main/bmijs/bmi.js
 * Independently implemented; TypedArray/C++ strictness is an Explorer policy.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
import { BMIError, DTYPES, INT_FIELDS, buffer, indices, supports } from './contract.js';
import { scenarioData, SCENARIOS } from './scenarios.js';

/** One stateful model owns all grids and independently allocated primitive arrays.
 * JavaScript objects cannot promise C++ raw-pointer lifetime or memory safety.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export default class BMI {
  #state = 'new';
  #data;
  #variables = new Map();
  #values = new Map();
  #time = 0;
  #scenario = '';

  /** Read-only non-BMI teaching status. @returns {string} new/initialized/finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get lifecycleState() { return this.#state; }
  /** Read-only non-BMI scenario identity. @returns {string} Selected token.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get scenarioKey() { return this.#scenario; }

  /** Require live state before any BMI call. @returns {void}
   * @throws {BMIError} Call before initialization/after finalization.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  #live() {
    if (this.#state !== 'initialized') throw new BMIError('BMILifecycleError', `Model is ${this.#state}. This BMI call requires an initialized model. Reset creates a new owner; a retained JS array does not revive a finalized model.`);
  }

  /** Resolve a variable without coercing its name.
   * @param {string} name Variable identity. @param {string} method Calling method.
   * @returns {object} Immutable descriptor. @throws {BMIError} Invalid name/lifecycle.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  #variable(name, method) {
    this.#live();
    if (typeof name !== 'string' || !this.#variables.has(name)) throw new BMIError('BMIIndexError', `${method}: unknown variable ${String(name)}. Choose a name returned by get_output_var_names().`);
    return this.#variables.get(name);
  }

  /** Resolve grid identity and applicability before touching output memory.
   * @param {number} id Exact numeric ID. @param {string} method Calling method.
   * @returns {object} Frozen descriptor. @throws {BMIError} Invalid ID, family or axis.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  #grid(id, method) {
    this.#live();
    if (!Number.isInteger(id) || id < 0 || id >= this.#data.grids.length) throw new BMIError('BMIIndexError', `${method}: expected an integer grid ID from get_var_grid(name); received ${String(id)}.`);
    const grid = this.#data.grids[id];
    if (!supports(grid, method)) throw new BMIError('BMIGridOperationError', `${method}(grid=${id}): unavailable for ${grid.kind}, rank ${grid.rank}. Uniform grids use shape/spacing/origin; rectilinear grids use axis coordinates; points/meshes use node coordinates. Missing axes and scalar geometry are not zero arrays. Try an applicable method in the inspector.`);
    return grid;
  }

  /** Copy descriptor geometry into an exact, existing caller buffer.
   * @param {number} id Grid ID. @param {string} field Geometry field.
   * @param {TypedArray} dest Existing buffer. @returns {TypedArray} Identical destination.
   * @throws {BMIError} Invalid state, applicability or buffer; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  #geometry(id, field, dest) {
    const method = 'get_grid_' + field;
    const values = this.#grid(id, method)[field];
    buffer(dest, INT_FIELDS.includes(field) ? 'int32' : 'float64', values.length, method);
    dest.set(values);
    return dest;
  }

  /** Initialize once; the token is browser-local configuration, not a file path.
   * @param {string} config_file Scenario token or empty default. @returns {void}
   * @throws {BMIError} Invalid token/lifecycle; initialization is atomic.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  initialize(config_file) {
    if (this.#state !== 'new') throw new BMIError('BMILifecycleError', 'initialize requires a new model. Use Reset for a fresh instance.');
    const key = config_file === '' ? 'all_grids' : config_file;
    if (typeof key !== 'string' || !Object.hasOwn(SCENARIOS, key)) throw new BMIError('BMIIndexError', `initialize: expected a registered browser scenario; received ${String(key)}.`);
    const data = scenarioData(key);
    const variables = new Map(data.variables.map(v => [v.name, v]));
    const values = new Map(data.variables.map(v => {
      const Type = DTYPES[v.dtype].ctor;
      const big = v.dtype === 'int64' || v.dtype === 'uint64';
      return [v.name, new Type(v.initial.map(n => big ? BigInt(n) : n))];
    }));
    this.#data = data;
    this.#variables = variables;
    this.#values = values;
    this.#scenario = key;
    this.#time = 0;
    this.#state = 'initialized';
  }

  /** Advance every evolving variable together by one timestep. @returns {void}
   * @throws {BMIError} Invalid lifecycle or end time; no partial updates.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  update() { this.#live(); this.update_until(this.#time + 3600); }

  /** Advance to an exact step boundary; typed-width examples stay static.
   * @param {number} time Absolute seconds. @returns {void}
   * @throws {BMIError} Non-finite, fractional, backwards or beyond-end target.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  update_until(time) {
    this.#live();
    if (typeof time !== 'number' || !Number.isFinite(time)) throw new BMIError('BMITypeError', 'update_until: expected finite numeric seconds, not a string or boolean.');
    if (time < this.#time || time > 10800 || time % 3600 !== 0) throw new BMIError('BMILifecycleError', `update_until: require ${this.#time} ≤ time ≤ 10800 at a 3600 s boundary. Fractional steps are unsupported by this fixture, not by all BMI models.`);
    const steps = (time - this.#time) / 3600;
    if (steps === 0) return;
    for (const [name, values] of this.#values) if (this.#variables.get(name).evolving) {
      for (let i = 0; i < values.length; i += 1) values[i] += steps;
    }
    this.#time = time;
  }

  /** Invalidate all subsequent BMI calls; retained JS arrays may survive. @returns {void}
   * @throws {BMIError} Not initialized/already finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  finalize() { this.#live(); this.#values.clear(); this.#state = 'finalized'; }

  /** Expose immutable descriptors to the teaching UI, outside the BMI surface.
   * @param {number} id Grid ID. @returns {object} Frozen geometry metadata.
   * @throws {BMIError} Invalid lifecycle or ID.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  describeGrid(id) { return this.#grid(id, 'get_grid_type'); }

  /** Expose immutable variable metadata, outside BMI.
   * @param {string} name Variable name. @returns {object} Frozen descriptor.
   * @throws {BMIError} Invalid lifecycle or variable.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  describeVariable(name) { return this.#variable(name, 'describeVariable'); }

  /** Return node count independently of variable location cardinality.
   * @param {object} grid Descriptor. @returns {number} Nodes (scalar has one).
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  #size(grid) { return grid.shape.length ? grid.shape.reduce((a, b) => a * b, 1) : grid.x.length || 1; }

  /** Return live primitive storage, preserving object identity through setters.
   * @param {string} name Variable name. @returns {TypedArray} Model-owned alias.
   * @throws {BMIError} Invalid lifecycle/name.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_value_ptr(name) { this.#variable(name, 'get_value_ptr'); return this.#values.get(name); }

  /** Copy to the caller's buffer; the copy never aliases model state.
   * @param {string} name Variable name. @param {TypedArray} dest Exact output.
   * @returns {TypedArray} The identical dest. @throws {BMIError} Failed validation; no writes.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_value(name, dest) {
    const variable = this.#variable(name, 'get_value');
    const values = this.#values.get(name);
    buffer(dest, variable.dtype, values.length, 'get_value');
    dest.set(values.slice());
    return dest;
  }

  /** Copy full input in place without broadcasting or casting.
   * @param {string} name Variable name. @param {TypedArray} src Exact input buffer.
   * @returns {void} @throws {BMIError} Failed validation; model unchanged.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  set_value(name, src) {
    const variable = this.#variable(name, 'set_value');
    const values = this.#values.get(name);
    buffer(src, variable.dtype, values.length, 'set_value');
    values.set(src.slice());
  }

  /** Copy selected flat variable values, staging overlapping input/destination.
   * @param {string} name Variable name. @param {TypedArray} dest Exact output.
   * @param {Int32Array} inds Flat indices. @returns {TypedArray} Same destination.
   * @throws {BMIError} Invalid indices/dtype/count; no destination writes.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_value_at_indices(name, dest, inds) {
    const variable = this.#variable(name, 'get_value_at_indices');
    const values = this.#values.get(name);
    indices(inds, values.length, 'get_value_at_indices');
    buffer(dest, variable.dtype, inds.length, 'get_value_at_indices');
    const staged = new values.constructor(inds.length);
    for (let i = 0; i < inds.length; i += 1) staged[i] = values[inds[i]];
    dest.set(staged);
    return dest;
  }

  /** Write selected values; repeated indices use the last staged source value.
   * @param {string} name Variable name. @param {Int32Array} inds Flat indices.
   * @param {TypedArray} src One exact-width value per index. @returns {void}
   * @throws {BMIError} Validation failure; model unchanged.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  set_value_at_indices(name, inds, src) {
    const variable = this.#variable(name, 'set_value_at_indices');
    const values = this.#values.get(name);
    indices(inds, values.length, 'set_value_at_indices');
    buffer(src, variable.dtype, inds.length, 'set_value_at_indices');
    const selected = inds.slice();
    const staged = src.slice();
    for (let i = 0; i < selected.length; i += 1) values[selected[i]] = staged[i];
  }

  /** Return component name for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_component_name() { this.#live(); return 'BMI Explorer (JavaScript)'; }

  /** Return input item count for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_input_item_count() { this.#live(); return this.get_input_var_names().length; }

  /** Return output item count for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_output_item_count() { this.#live(); return this.get_output_var_names().length; }

  /** Return input var names for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_input_var_names() { this.#live(); return Object.freeze([...this.#variables.values()].filter(v => v.writable).map(v => v.name)); }

  /** Return output var names for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_output_var_names() { this.#live(); return Object.freeze([...this.#variables.values()].filter(v => v.readable).map(v => v.name)); }

  /** Return current time for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_current_time() { this.#live(); return this.#time; }

  /** Return start time for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_start_time() { this.#live(); return 0; }

  /** Return end time for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_end_time() { this.#live(); return 10800; }

  /** Return time units for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_time_units() { this.#live(); return 's'; }

  /** Return time step for the live model.
   * @returns {number|string|ReadonlyArray<string>} Declared model metadata.
   * @throws {BMIError} Model is not initialized or has been finalized.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_time_step() { this.#live(); return 3600; }

  /** Return the declared variable grid.
   * @param {string} name Exact exposed variable name. @returns {number|string} Immutable metadata.
   * @throws {BMIError} Invalid name or lifecycle.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_var_grid(name) { const variable = this.#variable(name, 'get_var_grid'); return variable.grid; }

  /** Return the declared variable type.
   * @param {string} name Exact exposed variable name. @returns {number|string} Immutable metadata.
   * @throws {BMIError} Invalid name or lifecycle.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_var_type(name) { const variable = this.#variable(name, 'get_var_type'); return variable.primitive; }

  /** Return the declared variable units.
   * @param {string} name Exact exposed variable name. @returns {number|string} Immutable metadata.
   * @throws {BMIError} Invalid name or lifecycle.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_var_units(name) { const variable = this.#variable(name, 'get_var_units'); return variable.units; }

  /** Return the declared variable location.
   * @param {string} name Exact exposed variable name. @returns {number|string} Immutable metadata.
   * @throws {BMIError} Invalid name or lifecycle.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_var_location(name) { const variable = this.#variable(name, 'get_var_location'); return variable.location; }

  /** Return the declared variable itemsize.
   * @param {string} name Exact exposed variable name. @returns {number|string} Immutable metadata.
   * @throws {BMIError} Invalid name or lifecycle.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_var_itemsize(name) { const variable = this.#variable(name, 'get_var_itemsize'); return DTYPES[variable.dtype].ctor.BYTES_PER_ELEMENT; }

  /** Return the declared variable nbytes.
   * @param {string} name Exact exposed variable name. @returns {number|string} Immutable metadata.
   * @throws {BMIError} Invalid name or lifecycle.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_var_nbytes(name) { const variable = this.#variable(name, 'get_var_nbytes'); return this.#values.get(name).byteLength; }

  /** Return grid type; empty topology counts are zero.
   * @param {number} grid ID from get_var_grid. @returns {number|string} Declared grid metadata.
   * @throws {BMIError} Invalid lifecycle, ID or topology applicability.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_type(grid) { const descriptor = this.#grid(grid, 'get_grid_type'); return descriptor.kind; }

  /** Return grid rank; empty topology counts are zero.
   * @param {number} grid ID from get_var_grid. @returns {number|string} Declared grid metadata.
   * @throws {BMIError} Invalid lifecycle, ID or topology applicability.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_rank(grid) { const descriptor = this.#grid(grid, 'get_grid_rank'); return descriptor.rank; }

  /** Return grid size; empty topology counts are zero.
   * @param {number} grid ID from get_var_grid. @returns {number|string} Declared grid metadata.
   * @throws {BMIError} Invalid lifecycle, ID or topology applicability.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_size(grid) { const descriptor = this.#grid(grid, 'get_grid_size'); return this.#size(descriptor); }

  /** Return grid node count; empty topology counts are zero.
   * @param {number} grid ID from get_var_grid. @returns {number|string} Declared grid metadata.
   * @throws {BMIError} Invalid lifecycle, ID or topology applicability.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_node_count(grid) { const descriptor = this.#grid(grid, 'get_grid_node_count'); return this.#size(descriptor); }

  /** Return grid edge count; empty topology counts are zero.
   * @param {number} grid ID from get_var_grid. @returns {number|string} Declared grid metadata.
   * @throws {BMIError} Invalid lifecycle, ID or topology applicability.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_edge_count(grid) { const descriptor = this.#grid(grid, 'get_grid_edge_count'); return descriptor.edge_nodes.length / 2; }

  /** Return grid face count; empty topology counts are zero.
   * @param {number} grid ID from get_var_grid. @returns {number|string} Declared grid metadata.
   * @throws {BMIError} Invalid lifecycle, ID or topology applicability.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_face_count(grid) { const descriptor = this.#grid(grid, 'get_grid_face_count'); return descriptor.nodes_per_face.length; }

  /** Copy shape into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} shape Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_shape(grid, shape) { return this.#geometry(grid, 'shape', shape); }

  /** Copy spacing into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} spacing Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_spacing(grid, spacing) { return this.#geometry(grid, 'spacing', spacing); }

  /** Copy origin into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} origin Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_origin(grid, origin) { return this.#geometry(grid, 'origin', origin); }

  /** Copy x into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} x Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_x(grid, x) { return this.#geometry(grid, 'x', x); }

  /** Copy y into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} y Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_y(grid, y) { return this.#geometry(grid, 'y', y); }

  /** Copy z into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} z Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_z(grid, z) { return this.#geometry(grid, 'z', z); }

  /** Copy edge nodes into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} edge_nodes Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_edge_nodes(grid, edge_nodes) { return this.#geometry(grid, 'edge_nodes', edge_nodes); }

  /** Copy face edges into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} face_edges Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_face_edges(grid, face_edges) { return this.#geometry(grid, 'face_edges', face_edges); }

  /** Copy face nodes into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} face_nodes Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_face_nodes(grid, face_nodes) { return this.#geometry(grid, 'face_nodes', face_nodes); }

  /** Copy nodes per face into exact caller-owned output memory.
   * @param {number} grid ID from get_var_grid. @param {TypedArray} nodes_per_face Exact native output buffer.
   * @returns {TypedArray} Same destination; empty topology requires zero length.
   * @throws {BMIError} Lifecycle, applicability or buffer failure; no writes occur.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  get_grid_nodes_per_face(grid, nodes_per_face) { return this.#geometry(grid, 'nodes_per_face', nodes_per_face); }
}
