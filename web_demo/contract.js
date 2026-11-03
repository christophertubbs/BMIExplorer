/** Strict JavaScript buffer contracts and operation applicability.
 * TypedArray strictness is an Explorer policy inspired by C++ caller-owned memory.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */

/** Named, actionable contract violation; never repairs its inputs.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export class BMIError extends Error {
  /** @param {string} name Error category. @param {string} message Expected versus received contract.
   * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
   * TODO: AI-generated implementation; human review and rewrite required.
   */
  constructor(name, message) { super(message); this.name = name; }
}

export const DTYPES = Object.freeze({
  int8: Object.freeze({ ctor: Int8Array, primitive: 'signed char', min: -128, max: 127 }),
  uint8: Object.freeze({ ctor: Uint8Array, primitive: 'unsigned char', min: 0, max: 255 }),
  int16: Object.freeze({ ctor: Int16Array, primitive: 'short', min: -32768, max: 32767 }),
  uint16: Object.freeze({ ctor: Uint16Array, primitive: 'unsigned short', min: 0, max: 65535 }),
  int32: Object.freeze({ ctor: Int32Array, primitive: 'int', min: -2147483648, max: 2147483647 }),
  uint32: Object.freeze({ ctor: Uint32Array, primitive: 'unsigned int', min: 0, max: 4294967295 }),
  int64: Object.freeze({ ctor: BigInt64Array, primitive: 'long long', min: -(2n ** 63n), max: 2n ** 63n - 1n }),
  uint64: Object.freeze({ ctor: BigUint64Array, primitive: 'unsigned long long', min: 0n, max: 2n ** 64n - 1n }),
  float32: Object.freeze({ ctor: Float32Array, primitive: 'float' }),
  float64: Object.freeze({ ctor: Float64Array, primitive: 'double' }),
});

export const GRID_METHODS = Object.freeze([
  'get_grid_type', 'get_grid_rank', 'get_grid_size', 'get_grid_shape',
  'get_grid_spacing', 'get_grid_origin', 'get_grid_x', 'get_grid_y', 'get_grid_z',
  'get_grid_node_count', 'get_grid_edge_count', 'get_grid_face_count',
  'get_grid_edge_nodes', 'get_grid_face_nodes', 'get_grid_face_edges', 'get_grid_nodes_per_face',
]);
export const VALUE_METHODS = Object.freeze(['get_value', 'get_value_ptr', 'get_value_at_indices', 'set_value', 'set_value_at_indices']);
export const VARIABLE_METHODS = Object.freeze(['get_var_grid', 'get_var_type', 'get_var_units', 'get_var_itemsize', 'get_var_nbytes', 'get_var_location']);
export const INFO_METHODS = Object.freeze(['get_component_name', 'get_input_item_count', 'get_output_item_count', 'get_input_var_names', 'get_output_var_names', 'get_current_time', 'get_start_time', 'get_end_time', 'get_time_units', 'get_time_step']);
export const BMI_METHODS = Object.freeze(['initialize', 'update', 'update_until', 'finalize', ...INFO_METHODS, ...VARIABLE_METHODS, ...VALUE_METHODS, ...GRID_METHODS]);
const STRUCTURED = ['uniform_rectilinear', 'rectilinear'];
const EXPLICIT = ['rectilinear', 'points', 'unstructured'];
const TOPOLOGY = ['points', 'unstructured'];
export const INT_FIELDS = Object.freeze(['shape', 'edge_nodes', 'face_nodes', 'face_edges', 'nodes_per_face']);

/** Recursively freeze metadata, not mutable model value buffers.
 * @param {object} value Plain metadata tree. @returns {object} The frozen tree.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function deepFreeze(value) {
  for (const child of Object.values(value)) if (child && typeof child === 'object') deepFreeze(child);
  return Object.freeze(value);
}

/** Require an actual native contiguous typed buffer with the exact primitive width.
 * @param {unknown} value Caller memory. @param {string} dtype Required width.
 * @param {number|null} count Exact elements, or null for any length.
 * @param {string} context Calling operation. @returns {TypedArray} Original buffer.
 * @throws {BMIError} Wrong dtype, layout, detached, shared or resizable buffer; no writes.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function buffer(value, dtype, count, context) {
  const Type = DTYPES[dtype]?.ctor;
  const received = value === null ? 'null' : value?.constructor?.name ?? typeof value;
  if (!Type || !ArrayBuffer.isView(value) || !(value instanceof Type) || Object.getPrototypeOf(value) !== Type.prototype) {
    throw new BMIError('BMITypeError', `${context}: expected ${Type?.name ?? dtype}(${count ?? 'N'}); received ${received}. C++ consumes an existing buffer of the declared primitive type. Allocate the exact TypedArray; no arrays, casts or broadcasting are accepted.`);
  }
  if (!(value.buffer instanceof ArrayBuffer) || value.buffer.resizable) {
    throw new BMIError('BMIBufferError', `${context}: use a fixed, non-shared ArrayBuffer. Explorer rejects concurrent resizing/sharing during a call.`);
  }
  try { value.subarray(0, 0); } catch { throw new BMIError('BMIBufferError', `${context}: this buffer is detached; allocate fresh caller memory.`); }
  if (count !== null && value.length !== count) {
    throw new BMIError('BMIBufferError', `${context}: expected ${Type.name}(${count}), received ${Type.name}(${value.length}). Length is a contract, not a request to resize or broadcast. No destination or model values were changed.`);
  }
  return value;
}

/** Validate indexed calls against the variable's cardinality, not grid size.
 * @param {unknown} inds Caller index memory. @param {number} count Variable count.
 * @param {string} context Calling method. @returns {Int32Array} Same validated indices.
 * @throws {BMIError} Wrong width or out-of-range indices; no writes.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function indices(inds, count, context) {
  buffer(inds, 'int32', null, context);
  for (const index of inds) if (index < 0 || index >= count) {
    throw new BMIError('BMIIndexError', `${context}: index ${index} is outside 0 ≤ index < ${count}. These are flat variable-value indices; node, edge and face variables have different bounds. Try index 0.`);
  }
  return inds;
}

/** Determine family and active-axis applicability for one descriptor.
 * @param {object} grid Frozen grid metadata. @param {string} method BMI method name.
 * @returns {boolean} Whether this call has meaningful geometry for the grid.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function supports(grid, method) {
  if (!GRID_METHODS.includes(method) || ['get_grid_type', 'get_grid_rank', 'get_grid_size'].includes(method)) return true;
  if (method === 'get_grid_shape') return STRUCTURED.includes(grid.kind);
  if (['get_grid_origin', 'get_grid_spacing'].includes(method)) return grid.kind === 'uniform_rectilinear';
  const axis = ['get_grid_x', 'get_grid_y', 'get_grid_z'].indexOf(method);
  if (axis !== -1) return EXPLICIT.includes(grid.kind) && grid.rank > axis;
  return TOPOLOGY.includes(grid.kind);
}

/** Convert UI text explicitly into caller-owned memory without silent numeric wrap.
 * @param {string} text Comma/space-separated values. @param {string} dtype Width.
 * @returns {TypedArray} New exact-width buffer; BigInt text preserves 64-bit precision.
 * @throws {BMIError} Invalid syntax, overflow or integer fraction, before allocation.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function parseBuffer(text, dtype) {
  const spec = DTYPES[dtype];
  if (!spec) throw new BMIError('BMITypeError', `Unknown dtype ${dtype}.`);
  const tokens = text.trim() ? text.trim().split(/[\s,]+/) : [];
  const values = tokens.map(token => {
    const big = dtype === 'int64' || dtype === 'uint64';
    let value;
    if (big) {
      if (!/^[+-]?\d+$/.test(token)) throw new BMIError('BMITypeError', `Use integer text for ${dtype}; received ${token}.`);
      value = BigInt(token);
    } else {
      value = Number(token);
      if (!Number.isFinite(value) || (spec.min !== undefined && !Number.isInteger(value))) throw new BMIError('BMITypeError', `${token} is not a finite ${dtype} value. No implicit integer truncation.`);
      if (dtype === 'float32' && !Number.isFinite(Math.fround(value))) throw new BMIError('BMITypeError', `${token} overflows float32.`);
    }
    if (spec.min !== undefined && (value < spec.min || value > spec.max)) throw new BMIError('BMITypeError', `${token} is outside ${dtype}'s range [${spec.min}, ${spec.max}]. No wrapping or signedness conversion.`);
    return value;
  });
  return new spec.ctor(values);
}
