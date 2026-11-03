/** Shared method metadata for tactile controls, traces and contract tests.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
import { BMI_METHODS, GRID_METHODS, VALUE_METHODS, VARIABLE_METHODS, INT_FIELDS, supports } from './contract.js';

/** Describe how to allocate and invoke one BMI method without executing it.
 * @param {string} method Exact BMI method. @param {object} grid Immutable grid.
 * @param {object} variable Immutable variable. @param {number} indexCount Selected indices count.
 * @returns {object} Invocation/teaching metadata for the current selection.
 * @throws {RangeError} Method outside the BMI surface.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function operationSpec(method, grid, variable, indexCount = 1) {
  if (!BMI_METHODS.includes(method)) throw new RangeError(`Unknown BMI method ${method}.`);
  const field = method.replace('get_grid_', '');
  const gridCall = GRID_METHODS.includes(method);
  const indexed = method.endsWith('_at_indices');
  const setter = method.startsWith('set_value');
  const geometry = gridCall && Array.isArray(grid[field]);
  const valueBuffer = VALUE_METHODS.includes(method) && method !== 'get_value_ptr';
  const hasBuffer = geometry || valueBuffer;
  const count = geometry ? grid[field].length : indexed ? indexCount : variable.initial.length;
  const dtype = geometry ? INT_FIELDS.includes(field) ? 'int32' : 'float64' : variable.dtype;
  const applicable = !gridCall || supports(grid, method);
  const context = gridCall ? `grid ${variable.grid} · ${grid.kind} · rank ${grid.rank}` : variable.name;
  const parameter = gridCall ? `grid=${variable.grid}` : VALUE_METHODS.includes(method) || VARIABLE_METHODS.includes(method) ? `'${variable.name}'` : method === 'update_until' ? 'time' : method === 'initialize' ? 'scenario' : '';
  const signature = `${method}(${parameter}${indexed && setter ? ', inds, src' : hasBuffer ? (setter ? ', src' : ', dest') + (indexed ? ', inds' : '') : ''})`;
  let lesson = 'BMI REQUIRED · query explicit model metadata; a grid ID identifies geometry, not a variable.';
  if (geometry) lesson = `GRID-TYPE APPLICABILITY · ${field} uses ${dtype} with ${count} elements on this grid. ` + (['x', 'y', 'z'].includes(field) ? grid.kind === 'rectilinear' ? 'One coordinate per axis position, not per node.' : 'One coordinate per node on an active physical axis.' : field === 'shape' ? 'Shape counts nodes in ij order: [nz, ny, nx].' : 'Connectivity buffers use zero-based IDs and ragged face offsets.');
  if (['spacing', 'origin'].includes(field)) lesson = 'GRID-TYPE APPLICABILITY · uniform geometry uses [dy, dx] or [dz, dy, dx]. These methods do not apply to scalar, points, unstructured or nonuniform rectilinear grids.';
  if (!applicable) lesson = `GRID-TYPE APPLICABILITY · ${method} is unavailable for ${grid.kind}, rank ${grid.rank}. Try it: a controlled error should preserve every destination and model value.`;
  if (valueBuffer) lesson = `C++ PARITY · ${setter ? 'write' : 'read'} ${indexed ? 'one value per Int32Array index' : 'the complete variable'} through existing ${dtype} memory. Wrong primitive widths, counts and plain arrays are rejected before writes.`;
  if (method === 'get_value_ptr') lesson = 'BMI REQUIRED · returns a live alias, not a copy. Editing retained reference elements changes model state immediately. JavaScript cannot reproduce dangling C++ pointers after owner destruction.';
  if (['initialize', 'finalize', 'update', 'update_until'].includes(method)) lesson = 'EXPLORER POLICY · all nine grids share one lifecycle and clock. Steps are 3600 s; end is 10800 s. Only a new object can initialize. Finalization rejects every later BMI call.';
  return { method, field, gridCall, indexed, setter, geometry, valueBuffer, hasBuffer, count, dtype, applicable, context, signature, lesson };
}
