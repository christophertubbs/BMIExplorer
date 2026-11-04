/** Tactile BMI composition: views observe one JS model; every mutation is explicit.
 * No eval, Python calls, backend endpoints, persistence or hosted services.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
import BMI from './bmi.js';
import { BMIError, DTYPES, BMI_METHODS, GRID_METHODS, VALUE_METHODS, VARIABLE_METHODS, INFO_METHODS, parseBuffer, supports } from './contract.js';
import { SCENARIOS } from './scenarios.js';
import { operationSpec } from './operations.js';
import { drawGrid } from './visualization.js';
import { byId, node, option, format, inputText } from './ui.js';

/** @type {{model:BMI, variable:string, index:number, grid:object|null, descriptor:object|null, memory:object|null, sequence:number, snapshot:TypedArray|null}} */
const state = { model: new BMI(), variable: 'uniform_3d__soil_temp', index: 0, grid: null, descriptor: null, memory: null, sequence: 0, snapshot: null };
state.model.initialize('all_grids');

/** Return all current grid IDs through public BMI variable discovery.
 * @returns {number[]} Unique IDs, preserving fixture order. @throws {BMIError} Model not live.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function gridIds() { return [...new Set([...state.model.get_output_var_names(), ...state.model.get_input_var_names()].map(name => state.model.get_var_grid(name)))]; }

/** Append an immutable textual experiment record and announce its result.
 * @param {string} call Exact operation display. @param {unknown} result Returned result/error.
 * @param {boolean} error Whether the call was rejected. @param {string} note Educational consequence.
 * @returns {void} Updates accessible result and bounded trace; never model state.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function record(call, result, error = false, note = '') {
  state.sequence += 1;
  const text = result instanceof Error ? `${result.name}: ${result.message}` : format(result);
  const latest = byId('latest-result');
  latest.textContent = `${error ? 'REJECTED' : 'ACCEPTED'} · ${call}\n${text}${note ? '\n' + note : ''}`;
  latest.classList.toggle('error', error);
  const row = node('li', '', 'trace-row' + (error ? ' error' : ''));
  row.append(node('span', String(state.sequence).padStart(3, '0'), 'trace-id'));
  const content = node('div');
  content.append(node('code', call), node('p', text + (note ? '\n' + note : '')));
  row.append(content, node('span', error ? 'REJECTED' : 'ACCEPTED', 'trace-badge'));
  byId('trace').prepend(row);
  while (byId('trace').children.length > 16) byId('trace').lastElementChild.remove();
}

/** Execute one explicit experiment, preserving errors for teaching rather than repairing them.
 * @param {string|Function} label Displayed operation or deferred exact invocation. @param {Function} action Model/UI action.
 * @param {string} note Educational consequence. @returns {unknown} Result or undefined after failure.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function attempt(label, action, note = '') {
  try {
    const result = action();
    record(typeof label === 'function' ? label() : label, result, false, note);
    refresh();
    return result;
  } catch (error) {
    record(typeof label === 'function' ? label() : label, error, true, error instanceof BMIError ? 'No automatic repair. Failed contract validation occurs before writes.' : 'The call was not repaired. Check the supplied values.');
    refresh();
    return undefined;
  }
}

/** Refresh clock/lifecycle without querying a finalized model.
 * @returns {void} Last spatial snapshot remains explicitly marked after finalize.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function refreshLifecycle() {
  const live = state.model.lifecycleState === 'initialized';
  byId('model-status').textContent = state.model.lifecycleState.toUpperCase();
  byId('model-status').classList.toggle('finalized', !live);
  if (live) byId('model-time').textContent = state.model.get_current_time().toLocaleString('en-US') + ' s';
  byId('plot-empty').hidden = live;
  byId('scope-note').textContent = live
    ? 'Switching models creates a fresh owner. Selecting grids and variables keeps this model and its clock.'
    : 'Finalized owner · spatial values are the last snapshot. BMI calls now fail; retained JS references may still exist. Reset creates a fresh model.';
}

/** Render one independently selectable inventory entry for every exposed variable.
 * @returns {void} Rebuilds metadata navigation; selections do not replace the model.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function renderInventory() {
  const host = byId('inventory');
  host.replaceChildren();
  const allNames = state.model.get_output_var_names();
  for (const id of gridIds()) {
    const grid = state.model.describeGrid(id);
    const section = node('div', '', 'inventory-group');
    const button = node('button', '', 'inventory-grid' + (id === state.descriptor.grid ? ' active' : ''));
    button.type = 'button'; button.dataset.grid = id;
    button.append(node('span', String(id).padStart(2, '0'), 'grid-num'), node('span', grid.label), node('span', 'r' + grid.rank, 'rank-label'));
    button.setAttribute('aria-label', `Select ${grid.label}, grid ${id}, rank ${grid.rank}`);
    button.onclick = () => selectVariable(`${grid.label}__value`);
    section.append(button);
    for (const name of allNames.filter(n => state.model.get_var_grid(n) === id)) {
      const variable = state.model.describeVariable(name);
      const item = node('button', '', 'variable-link' + (name === state.variable ? ' active' : ''));
      item.type = 'button'; item.dataset.variable = name;
      item.title = `${name}: ${variable.location}, ${variable.dtype}, ${variable.initial.length} values, ${state.model.get_var_nbytes(name)} bytes`;
      item.setAttribute('aria-pressed', String(name === state.variable));
      item.append(node('span', '', 'variable-dot'), node('span', name.replace(grid.label + '__', '')),
        node('span', `${variable.location === 'node' ? 'n' : variable.location[0]}·${variable.initial.length}`, 'type-hint'));
      item.onclick = () => selectVariable(name);
      section.append(item);
    }
    host.append(section);
  }
}

/** Build a simultaneously visible D3 representation of every grid and variable.
 * @returns {void} Every variable has a selectable labeled chip in its grid card.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function renderAtlas() {
  const host = byId('atlas');
  host.replaceChildren();
  for (const id of gridIds()) {
    const grid = state.model.describeGrid(id);
    const card = node('article', '', 'atlas-card' + (id === state.descriptor.grid ? ' active' : ''));
    const button = node('button', '', 'atlas-open');
    button.type = 'button'; button.dataset.atlasGrid = id;
    button.append(node('h3', `${String(id).padStart(2, '0')} / ${grid.label}`), node('p', `rank ${grid.rank} · ${state.model.get_grid_size(id)} nodes`, 'atlas-meta'));
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('aria-hidden', 'true');
    button.append(svg);
    button.onclick = () => { selectVariable(`${grid.label}__value`); setView(false); };
    card.append(button);
    const variables = node('div', '', 'atlas-vars');
    for (const name of state.model.get_output_var_names().filter(n => state.model.get_var_grid(n) === id)) {
      const descriptor = state.model.describeVariable(name);
      const chip = node('button', `${name.replace(grid.label + '__', '')} · ${descriptor.dtype} [${descriptor.initial.length}]`);
      chip.title = name;
      chip.type = 'button'; chip.dataset.atlasVariable = name;
      chip.onclick = () => { selectVariable(name); setView(false); };
      variables.append(chip);
    }
    card.append(variables); host.append(card);
    drawGrid(svg, grid, state.model.get_value_ptr(`${grid.label}__value`), { mini: true });
  }
}

/** Render immutable geometry facts and the selected variable's spatial association.
 * @returns {void} Updates plot, shape/count metadata, projection controls and value legend.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function renderGrid() {
  const grid = state.grid;
  const variable = state.descriptor;
  const model = state.model;
  byId('grid-title').textContent = grid.label;
  byId('grid-type').textContent = grid.kind.replaceAll('_', ' ').toUpperCase();
  byId('grid-id').textContent = 'GRID ' + String(variable.grid).padStart(2, '0');
  const facts = byId('grid-facts'); facts.replaceChildren();
  const entries = [['RANK', grid.rank], ['GRID SIZE', model.get_grid_size(variable.grid)], ['SHAPE · IJ', grid.shape.length ? '[' + grid.shape.join(', ') + ']' : 'not applicable'], ['VALUE COUNT', variable.initial.length]];
  for (const [label, value] of entries) { const item = node('div'); item.append(node('dt', label), node('dd', String(value))); facts.append(item); }
  byId('rotation-control').hidden = grid.rank !== 3;
  drawGrid(byId('main-grid'), grid, state.snapshot, { selected: state.index, location: variable.location, labels: byId('show-labels').checked, angle: Number(byId('rotation').value) * Math.PI / 180, onSelect: selectIndex });
  let note = 'Scalar rank is 0, yet one logical value still needs storage. Geometry methods should refuse this grid.';
  if (grid.kind === 'uniform_rectilinear') note = `Shape, spacing and origin define ${model.get_grid_size(variable.grid)} nodes. x varies fastest in flat C order. Lines in the plot are derived guides; BMI does not expose them as topology.`;
  if (grid.kind === 'rectilinear') note = `Coordinate buffers describe axis positions: x has ${grid.x.length} entries, y has ${grid.y.length}${grid.rank === 3 ? ', z has ' + grid.z.length : ''}. Their lengths differ from the ${model.get_grid_size(variable.grid)} node values. Uniform spacing is unavailable.`;
  if (grid.kind === 'points') note = `Each active coordinate array has ${grid.x.length} entries, one per node. Rank ${grid.rank} counts physical axes, not points. No connectivity joins these locations; empty topology is an explicit Explorer policy.`;
  if (grid.kind === 'unstructured') note = `${grid.x.length} nodes · ${grid.edge_nodes.length / 2} edges · ${grid.nodes_per_face.length} faces. The selected variable is at ${variable.location}s, so its ${variable.initial.length} values use ${variable.location} indices. ` + (grid.nodes_per_face.length ? 'Faces have [4, 4, 3] nodes; cumulative offsets delimit their flattened connectivity.' : 'An edge network has no faces. Exact empty face buffers are valid.');
  if (grid.rank === 3) note += ' This is a rotatable 3D projection, not a general volume/cell connectivity interface.';
  byId('geometry-note').textContent = note;
}

/** Render all flat values with keyboard/click selection and explicit indexed-write controls.
 * @returns {void} The visual strip remains connected to the selected variable's storage.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function renderValues() {
  const variable = state.descriptor;
  const model = state.model;
  byId('variable-title').textContent = variable.name;
  byId('variable-location').textContent = variable.location.toUpperCase();
  const facts = byId('variable-facts'); facts.replaceChildren();
  for (const text of [`grid ${variable.grid}`, `${variable.dtype} / ${model.get_var_type(variable.name)}`, `${variable.initial.length} values`, `${model.get_var_itemsize(variable.name)} B / value`, `${model.get_var_nbytes(variable.name)} B total`, `units ${variable.units}`]) facts.append(node('span', text));
  const strip = byId('value-strip'); strip.replaceChildren();
  [...state.snapshot].forEach((value, index) => {
    const button = node('button', '', 'value-chip' + (index === state.index ? ' selected' : ''));
    button.type = 'button'; button.dataset.valueIndex = index;
    button.setAttribute('aria-label', `${variable.location} index ${index}, value ${format(value)}`);
    button.setAttribute('aria-pressed', String(index === state.index));
    button.append(node('small', String(index).padStart(2, '0')), node('strong', format(value)));
    button.onclick = () => selectIndex(index); strip.append(button);
  });
  byId('selected-index').max = variable.initial.length - 1;
  byId('selected-index').value = state.index;
  byId('edit-value').value = inputText([state.snapshot[state.index]]);
}

/** Refresh retained copy/reference data and make owner lifetime explicit.
 * @returns {void} Never invokes BMI on an old/finalized owner.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function renderMemory() {
  const memory = state.memory;
  if (!memory) return;
  const live = memory.owner === state.model && state.model.lifecycleState === 'initialized';
  byId('memory-owner').textContent = `${memory.name} · ${memory.copy.constructor.name}(${memory.copy.length}) · captured from ${memory.scenario}`;
  byId('pointer-status').textContent = live ? 'LIVE ALIAS' : 'RETAINED OLD OWNER';
  byId('pointer-status').classList.toggle('invalid', !live);
  byId('pointer-note').textContent = live ? 'Changing this array changes model values. set_value writes in place and preserves this reference.' : 'This array still exists in JavaScript. It no longer belongs to the active live model; C++ raw pointers may be dangling after owner destruction. Editing it cannot revive or change the new model.';
  for (const [id, values] of [['copy-values', memory.copy], ['pointer-values', memory.pointer]]) {
    const host = byId(id); host.replaceChildren();
    [...values].forEach((value, index) => host.append(node('span', format(value), 'memory-cell' + (index === 0 ? ' first' : ''))));
  }
  byId('copy-edit').disabled = false; byId('pointer-edit').disabled = false;
}

/** Re-render read-only views after a successful action or controlled failure.
 * @returns {void} After finalization, only lifecycle/memory views refresh.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function refresh() {
  refreshLifecycle();
  if (state.model.lifecycleState === 'initialized') {
    state.descriptor = state.model.describeVariable(state.variable);
    state.grid = state.model.describeGrid(state.descriptor.grid);
    state.snapshot = state.model.get_value_ptr(state.variable).slice();
    renderInventory(); renderGrid(); renderValues();
    if (!byId('atlas').hidden) renderAtlas();
  }
  renderMemory();
}

/** Select a target variable without changing model identity, memory or clock.
 * @param {string} name Exposed name. @returns {void}
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function selectVariable(name) {
  if (state.model.lifecycleState !== 'initialized') { attempt(`get_var_grid('${name}')`, () => state.model.get_var_grid(name)); return; }
  state.variable = name; state.index = 0;
  byId('comparison').hidden = true;
  refresh(); prepareOperation();
}

/** Select a flat variable index from a plot, chip or explicit field.
 * @param {number} index Valid flat index. @returns {void}
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function selectIndex(index) {
  if (!Number.isInteger(index) || index < 0 || index >= state.descriptor.initial.length) return;
  state.index = index;
  byId('indices').value = String(index);
  refresh(); prepareOperation();
}

/** Toggle the overview without selecting/replacing a model.
 * @param {boolean} atlas Whether to show all-grid overview. @returns {void}
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function setView(atlas) {
  byId('atlas').hidden = !atlas; byId('workbench').hidden = atlas;
  byId('atlas-tab').setAttribute('aria-pressed', String(atlas));
  byId('workbench-tab').setAttribute('aria-pressed', String(!atlas));
  byId('view-caption').textContent = atlas ? 'ONE MODEL · ALL NINE GRIDS' : 'SELECTED GRID';
  if (atlas && state.model.lifecycleState === 'initialized') renderAtlas();
}

/** Show method contract and initialize explicit caller-allocation controls.
 * @param {boolean} allocate Whether to reset the caller allocation to the declared contract.
 * @returns {void} Errors never call this correction automatically.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function prepareOperation(allocate = true) {
  const indexCount = byId('indices').value.trim() ? byId('indices').value.trim().split(/[\s,]+/).length : 0;
  const spec = operationSpec(byId('method').value, state.grid, state.descriptor, indexCount);
  byId('call-signature').textContent = spec.signature;
  byId('call-context').textContent = spec.context;
  byId('allocation-fields').hidden = !spec.hasBuffer;
  byId('source-field').hidden = !spec.setter;
  byId('indices-field').hidden = !spec.indexed;
  byId('target-time-field').hidden = spec.method !== 'update_until';
  byId('applicability').textContent = spec.applicable ? 'APPLICABLE' : 'EXPECTED APPLICABILITY ERROR';
  byId('applicability').classList.toggle('invalid', !spec.applicable);
  byId('method-lesson').textContent = spec.lesson;
  byId('allocation-note').textContent = `Declared: ${DTYPES[spec.dtype].ctor.name}(${spec.count}) · ${DTYPES[spec.dtype].ctor.BYTES_PER_ELEMENT * spec.count} bytes`;
  if (allocate) {
    byId('buffer-type').value = spec.dtype;
    byId('buffer-length').value = spec.count;
    const values = state.snapshot;
    const selected = spec.indexed ? byId('indices').value.split(/[\s,]+/).filter(Boolean).map(Number).map(i => values[i] ?? (spec.dtype.includes('64') && typeof values[0] === 'bigint' ? 0n : 0)) : [...values];
    byId('source-values').value = inputText(selected);
  }
}

/** Construct exactly the caller memory chosen in the form; do not silently repair it.
 * @param {object} spec Operation contract. @returns {TypedArray|Array|number|DataView} Caller input.
 * @throws {BMIError} Invalid allocation count, source syntax or overflow before invocation.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function callerBuffer(spec) {
  const selected = byId('buffer-type').value;
  const count = Number(byId('buffer-length').value);
  if (!Number.isInteger(count) || count < 0 || count > 256) throw new BMIError('BMIBufferError', 'Caller allocation must have 0–256 elements in this small demo. This UI limit is not a BMI restriction.');
  const source = byId('source-values').value;
  if (selected === 'number') return Number(source);
  if (selected === 'array') return spec.setter ? source.trim() ? source.split(/[\s,]+/).map(Number) : [] : Array(count).fill(-99);
  if (selected === 'dataview') return new DataView(new ArrayBuffer(count * 8));
  if (spec.setter) {
    const values = parseBuffer(source, selected);
    if (values.length !== count) throw new BMIError('BMIBufferError', `Caller allocation says ${count} elements but source text has ${values.length}. No padding, truncation or implicit broadcast. Make the count and source agree explicitly.`);
    return values;
  }
  const Type = DTYPES[selected].ctor;
  return new Type(count).fill(selected === 'int64' || selected === 'uint64' ? 7n : selected.startsWith('uint') ? 99 : -99);
}

/** Invoke a chosen method from controls, including deliberately unsupported calls.
 * @returns {void} Records destination identity, mutations, or unchanged error sentinels.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function runCall() {
  const method = byId('method').value;
  const spec = operationSpec(method, state.grid, state.descriptor);
  let label = spec.signature;
  attempt(() => label, () => {
    const args = [];
    let caller;
    if (spec.gridCall) args.push(state.descriptor.grid);
    else if (VALUE_METHODS.includes(method) || VARIABLE_METHODS.includes(method)) args.push(state.variable);
    if (spec.hasBuffer) caller = callerBuffer(spec);
    if (method === 'initialize') args.push(byId('scenario').value);
    if (method === 'update_until') args.push(Number(byId('target-time').value));
    if (spec.indexed) {
      const inds = parseBuffer(byId('indices').value, 'int32');
      if (spec.setter) args.push(inds, caller); else args.push(caller, inds);
    } else if (spec.hasBuffer) args.push(caller);
    label = `${method}(${args.map(arg => typeof arg === 'string' ? `'${arg}'` : format(arg)).join(', ')})`;
    let result;
    try { result = state.model[method](...args); }
    catch (error) {
      if (caller !== undefined) error.message += `\nCaller buffer after rejection: ${format(caller)}.`;
      throw error;
    }
    if (method === 'get_value_ptr') return `${format(result)}\nThis is a live alias. Use the memory bench to retain and edit it.`;
    if (spec.hasBuffer && !spec.setter) return `${format(result)}\nReturned destination === caller destination: ${result === caller}`;
    return result;
  }, spec.setter ? 'Typed input copied into existing model storage; other variables retain their values.' : 'Model identity is unchanged. Geometry queries never allocate/resize caller output.');
}

/** Explicitly replace the entire model, invalidating the previous live owner.
 * @param {string} key Registered scenario. @returns {void} Retained arrays stay visibly detached.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function replaceModel(key) {
  attempt(`new BMI(); initialize('${key}')`, () => {
    const next = new BMI(); next.initialize(key);
    if (state.model.lifecycleState === 'initialized') state.model.finalize();
    state.model = next;
    state.index = 0;
    byId('scenario-description').textContent = SCENARIOS[key].description;
    byId('comparison').hidden = true;
    return 'All nine grids and every variable initialized together; shared time reset to 0 s.';
  }, 'Previously retained copy/reference buffers stay attached to their old owner, never the new model.');
  prepareOperation();
}

/** Capture copy and live reference for the memory bench through real BMI calls.
 * @returns {void} Captures current variable; updates trace and both memory cards.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function captureMemory() {
  attempt(`get_value('${state.variable}', dest) + get_value_ptr('${state.variable}')`, () => {
    const variable = state.model.describeVariable(state.variable);
    const copy = new DTYPES[variable.dtype].ctor(variable.initial.length);
    state.model.get_value(state.variable, copy);
    const pointer = state.model.get_value_ptr(state.variable);
    state.memory = { name: state.variable, scenario: state.model.scenarioKey, owner: state.model, copy, pointer, dtype: variable.dtype };
    return `${format(copy)}\nCopy === reference: ${copy === pointer} · shared buffer: ${copy.buffer === pointer.buffer}`;
  }, 'The copy belongs to the caller. The reference aliases model-owned storage.');
}

/** Change one retained buffer by explicit, range-checked client-side element assignment.
 * @param {boolean} pointer Whether to edit the model-owned alias. @returns {void}
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function editMemory(pointer) {
  const memory = state.memory;
  if (!memory) return;
  const values = pointer ? memory.pointer : memory.copy;
  const next = values[0] + (typeof values[0] === 'bigint' ? 10n : 10);
  attempt(`${pointer ? 'retained_reference' : 'caller_copy'}[0] += 10`, () => {
    values[0] = parseBuffer(String(next), memory.dtype)[0];
    return format(values);
  }, pointer ? memory.owner === state.model && state.model.lifecycleState === 'initialized' ? 'A direct write through a live alias changes the model immediately; this is not set_value.' : 'Old JavaScript array edited. The current model is unchanged. Never infer C++ pointer validity from surviving JS references.' : 'Only the caller-owned copy changed. Model values and the live reference are untouched.');
}

/** Compare two current grids without changing state; report coordinate and method differences.
 * @returns {void} Writes the comparison panel and an explicit trace record.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function compareGrids() {
  attempt('compare current grids (Explorer helper)', () => {
    const model = state.model;
    const a = state.descriptor.grid;
    const b = Number(byId('compare-grid').value);
    const describe = id => {
      const grid = model.describeGrid(id);
      const lengths = ['x', 'y', 'z'].filter(axis => supports(grid, 'get_grid_' + axis)).map(axis => `${axis}:${grid[axis].length}`).join(', ') || 'not exposed';
      const vars = model.get_output_var_names().filter(name => model.get_var_grid(name) === id).map(name => `${name} ${model.describeVariable(name).initial.length} values/${model.get_var_nbytes(name)} B`).join('; ');
      return `${grid.label} · grid ${id} · ${grid.kind} · rank ${grid.rank}\n${model.get_grid_size(id)} nodes; coordinates ${lengths}\n${vars}`;
    };
    const ga = model.describeGrid(a); const gb = model.describeGrid(b);
    const differences = GRID_METHODS.filter(method => supports(ga, method) !== supports(gb, method)).map(method => `${method}: ${supports(ga, method) ? ga.label : gb.label} only`).join('\n') || 'Same applicable methods; compare ranks, lengths and returned values.';
    const text = `${describe(a)}\n\n${describe(b)}\n\n${differences}\n\nSame BMI object · same clock · no state was reset.`;
    byId('comparison').textContent = text; byId('comparison').hidden = false;
    return text;
  });
}

/** Configure one deliberate invalid request and execute it without argument repair.
 * @param {string} mistake Named experiment. @returns {void}
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function deliberateMistake(mistake) {
  if (mistake === 'geometry') {
    const bad = state.grid.kind === 'uniform_rectilinear' ? 'get_grid_x' : 'get_grid_spacing';
    byId('method').value = bad; prepareOperation(); runCall(); return;
  }
  if (mistake === 'bounds') {
    byId('method').value = 'get_value_at_indices';
    byId('indices').value = String(state.descriptor.initial.length);
    prepareOperation(); runCall(); return;
  }
  byId('method').value = mistake === 'broadcast' ? 'set_value' : 'get_value';
  prepareOperation();
  if (mistake === 'array') byId('buffer-type').value = 'array';
  if (mistake === 'dtype') byId('buffer-type').value = state.descriptor.dtype === 'float32' ? 'float64' : 'float32';
  if (mistake === 'length') byId('buffer-length').value = state.descriptor.initial.length + 1;
  if (mistake === 'broadcast') { byId('buffer-type').value = 'number'; byId('source-values').value = '9'; }
  runCall();
}

/** Compose controls and event handlers once, then show the initial live model.
 * @returns {void} Installs only DOM listeners; no model simulation runs on a timer.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function initializeUI() {
  for (const [key, scenario] of Object.entries(SCENARIOS)) option(byId('scenario'), key, scenario.name);
  byId('scenario-description').textContent = SCENARIOS.all_grids.description;
  for (const [label, names] of [['Value access', VALUE_METHODS], ['Grid geometry & topology', GRID_METHODS], ['Variable metadata', VARIABLE_METHODS], ['Model & time', [...INFO_METHODS, 'initialize', 'update', 'update_until', 'finalize']]]) {
    const group = node('optgroup'); group.label = label;
    for (const name of names) option(group, name, name);
    byId('method').append(group);
  }
  byId('method').value = 'get_grid_shape';
  for (const [dtype, spec] of Object.entries(DTYPES)) option(byId('buffer-type'), dtype, spec.ctor.name);
  option(byId('buffer-type'), 'array', 'Array · invalid');
  option(byId('buffer-type'), 'number', 'Number · invalid broadcast');
  option(byId('buffer-type'), 'dataview', 'DataView · invalid');
  for (const id of gridIds()) option(byId('compare-grid'), id, state.model.describeGrid(id).label);
  byId('compare-grid').value = '3';
  byId('scenario').onchange = event => replaceModel(event.target.value);
  byId('reset').onclick = () => replaceModel(byId('scenario').value);
  byId('step').onclick = () => attempt('update()', () => state.model.update(), 'One shared clock advances every evolving node/edge/face variable. Static dtype samples stay fixed.');
  byId('finalize').onclick = () => attempt('finalize()', () => state.model.finalize(), 'Every later BMI call should fail. Reset creates a new model; old JS references can survive.');
  byId('method').onchange = () => prepareOperation();
  byId('indices').oninput = () => prepareOperation(false);
  byId('allocate-correct').onclick = () => prepareOperation();
  byId('run-call').onclick = runCall;
  byId('show-labels').onchange = refresh;
  byId('rotation').oninput = () => { if (state.model.lifecycleState === 'initialized') renderGrid(); };
  byId('selected-index').onchange = event => selectIndex(Number(event.target.value));
  byId('write-value').onclick = () => attempt(`set_value_at_indices('${state.variable}', Int32Array([${byId('selected-index').value}]), src)`, () => {
    const indices = parseBuffer(byId('selected-index').value, 'int32');
    const source = parseBuffer(byId('edit-value').value, state.descriptor.dtype);
    state.model.set_value_at_indices(state.variable, indices, source);
    return 'The indexed value changed in place. Other variables did not.';
  });
  byId('capture-memory').onclick = captureMemory;
  byId('copy-edit').onclick = () => editMemory(false);
  byId('pointer-edit').onclick = () => editMemory(true);
  byId('compare').onclick = compareGrids;
  byId('atlas-tab').onclick = () => setView(true);
  byId('workbench-tab').onclick = () => setView(false);
  byId('clear-trace').onclick = () => { byId('trace').replaceChildren(); byId('latest-result').textContent = 'Record cleared. Model state and retained buffers are unchanged.'; byId('latest-result').classList.remove('error'); };
  byId('open-guide').onclick = () => byId('guide').showModal();
  byId('start-guide').onclick = () => byId('guide').close();
  for (const button of document.querySelectorAll('[data-mistake]')) button.onclick = () => deliberateMistake(button.dataset.mistake);
  refresh(); prepareOperation();
  record("initialize('all_grids')", '9 grids · 21 variables · one live model · time 0 s.', false, 'No Python connection. All calls and storage are JavaScript in this page.');
}

try { initializeUI(); }
catch (error) {
  const message = node('div', `The demo could not start: ${error.message}. Check that all files, including vendor/d3.v7.9.0.min.js, are served together.`, 'fatal-message');
  message.setAttribute('role', 'alert'); document.body.append(message);
  console.error(error);
}
