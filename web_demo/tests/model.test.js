/** Behavioral contract and independent numeric examples for the browser-local BMI.
 * Run with node --test web_demo/tests/*.test.js; no browser, Python or packages required.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import BMI from '../bmi.js';
import { BMI_METHODS, GRID_METHODS, DTYPES, buffer, parseBuffer, supports } from '../contract.js';
import { scenarioData, SCENARIOS } from '../scenarios.js';
import { operationSpec } from '../operations.js';
import { geometryNodes, geometryLinks } from '../visualization.js';

/** Construct independent initialized storage for each experiment.
 * @param {string} scenario Browser-local token. @returns {BMI} Fresh live model.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function initialized(scenario = 'all_grids') { const model = new BMI(); model.initialize(scenario); return model; }

/** Match a named BMI failure rather than accidentally accepting a native JS error.
 * @param {Function} action Probe. @param {string} name Expected category. @returns {void}
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
function rejects(action, name) { assert.throws(action, error => error.name === name); }

const INVENTORY = [
  ['scalar', 'scalar', 0, 1], ['uniform_2d', 'uniform_rectilinear', 2, 12],
  ['uniform_3d', 'uniform_rectilinear', 3, 24], ['rectilinear_2d', 'rectilinear', 2, 12],
  ['rectilinear_3d', 'rectilinear', 3, 24], ['points_2d', 'points', 2, 6],
  ['points_3d', 'points', 3, 6], ['unstructured_edges', 'unstructured', 1, 4],
  ['unstructured_mixed', 'unstructured', 2, 6],
];
const ARRAYS = [
  [1, 'shape', [3, 4]], [1, 'spacing', [2, 5]], [1, 'origin', [10, 100]],
  [2, 'shape', [2, 3, 4]], [2, 'spacing', [7, 2, 5]], [2, 'origin', [0, 10, 100]],
  [3, 'shape', [3, 4]], [3, 'x', [100, 102, 107, 115]], [3, 'y', [10, 11, 14]],
  [4, 'shape', [2, 3, 4]], [4, 'x', [100, 102, 107, 115]], [4, 'y', [10, 11, 14]], [4, 'z', [0, 7]],
  [5, 'x', [0, 2, 3, 1, -1, 1]], [5, 'y', [0, 0, 2, 3, 2, 1]],
  [6, 'x', [0, 2, 3, 1, -1, 1]], [6, 'y', [0, 0, 2, 3, 2, 1]], [6, 'z', [0, 1, 4, 2, 5, 3]],
  [7, 'x', [0, 2, 5, 9]], [7, 'edge_nodes', [0, 1, 1, 2, 2, 3]],
  [8, 'x', [0, 2, 3, 1, -1, 1]], [8, 'y', [0, 0, 2, 3, 2, 1]],
  [8, 'edge_nodes', [0, 1, 1, 2, 2, 3, 3, 4, 4, 0, 1, 5, 3, 5, 0, 5]],
  [8, 'face_nodes', [1, 2, 3, 5, 3, 4, 0, 5, 0, 1, 5]],
  [8, 'face_edges', [1, 2, 6, 5, 3, 4, 7, 6, 0, 5, 7]], [8, 'nodes_per_face', [4, 4, 3]],
];
const INTEGER_FIELDS = ['shape', 'edge_nodes', 'face_nodes', 'face_edges', 'nodes_per_face'];

test('all 41 interface methods exist and metadata remains immutable', () => {
  const model = initialized();
  assert.equal(new Set(BMI_METHODS).size, 41);
  for (const method of BMI_METHODS) assert.equal(typeof model[method], 'function', method);
  assert.equal(model.get_input_item_count(), 21);
  assert.deepEqual(model.get_input_var_names(), model.get_output_var_names());
  assert.throws(() => { model.describeGrid(1).shape[0] = 100; }, TypeError);
  assert.throws(() => { model.describeVariable('uniform_2d__slope').grid = 0; }, TypeError);
  assert.throws(() => { model.get_output_var_names().push('missing'); }, TypeError);
});

test('nine grids coexist: variable identity, location, dtype and exact initial values', () => {
  const model = initialized();
  const ids = new Set(model.get_output_var_names().map(n => model.get_var_grid(n)));
  assert.deepEqual([...ids], [0, 1, 2, 3, 4, 5, 6, 7, 8]);
  for (const [label, type, rank, size] of INVENTORY) {
    const name = model.get_output_var_names().find(n => model.describeVariable(n).grid === INVENTORY.findIndex(row => row[0] === label)); const id = model.get_var_grid(name);
    assert.deepEqual([model.get_grid_type(id), model.get_grid_rank(id), model.get_grid_size(id)], [type, rank, size]);
    assert.deepEqual([...model.get_value_ptr(name)], model.describeVariable(name).initial);
    assert.equal(model.get_var_type(name), 'double');
    assert.equal(model.get_var_nbytes(name), size * 8);
    assert.equal(model.get_var_location(name), 'node');
  }
  assert.equal(model.get_grid_node_count(8), 6);
  assert.equal(model.get_grid_edge_count(8), 8);
  assert.equal(model.get_grid_face_count(8), 3);
  for (const [suffix, count] of [['flux', 8], ['precipitation_rate', 3]]) {
    const name = 'unstructured_mixed__' + suffix;
    assert.equal(model.get_var_grid(name), 8);
    assert.equal(model.get_var_nbytes(name), count * 8);
    rejects(() => model.get_value_at_indices(name, new Float64Array(1), new Int32Array([count])), 'BMIIndexError');
    model.get_value_at_indices(name, new Float64Array(1), new Int32Array([count - 1]));
  }
});

for (const [id, field, expected] of ARRAYS) {
  test(`exact ${field} on grid ${id}: caller identity and no geometry alias`, () => {
    const model = initialized(); const Type = INTEGER_FIELDS.includes(field) ? Int32Array : Float64Array;
    const dest = new Type(expected.length);
    assert.equal(model['get_grid_' + field](id, dest), dest);
    assert.deepEqual([...dest], expected);
    dest.fill(99);
    model['get_grid_' + field](id, dest);
    assert.deepEqual([...dest], expected);
  });
  for (const badKind of ['array', 'dtype', 'length', 'DataView']) {
    test(`${field} grid ${id} rejects ${badKind} before destination writes`, () => {
      const model = initialized(); const Type = INTEGER_FIELDS.includes(field) ? Int32Array : Float64Array;
      const bad = badKind === 'array' ? Array(expected.length).fill(7)
        : badKind === 'dtype' ? new Float32Array(expected.length).fill(7)
          : badKind === 'DataView' ? new DataView(new ArrayBuffer(expected.length * 8))
            : new Type(expected.length + 1).fill(7);
      const before = ArrayBuffer.isView(bad) && !(bad instanceof DataView) ? [...bad] : Array.isArray(bad) ? [...bad] : [];
      rejects(() => model['get_grid_' + field](id, bad), badKind === 'length' ? 'BMIBufferError' : 'BMITypeError');
      if (!(bad instanceof DataView)) assert.deepEqual([...bad], before);
    });
  }
}

for (let id = 0; id < 9; id += 1) {
  test(`unsupported grid ${id} operations leave destination and all values unchanged`, () => {
    const model = initialized(); const grid = model.describeGrid(id);
    const before = model.get_output_var_names().map(name => [...model.get_value_ptr(name)]);
    for (const method of GRID_METHODS.filter(method => !supports(grid, method))) {
      const dest = new Float64Array(17).fill(7);
      rejects(() => model[method](id, dest), 'BMIGridOperationError');
      assert.deepEqual([...dest], Array(17).fill(7));
    }
    assert.deepEqual(model.get_output_var_names().map(name => [...model.get_value_ptr(name)]), before);
  });
}

test('missing axes and nonuniform geometry fail instead of fabricating coordinates', () => {
  const model = initialized();
  for (const id of [0, 1, 3, 5, 7, 8]) rejects(() => model.get_grid_z(id, new Float64Array(6)), 'BMIGridOperationError');
  for (const id of [0, 3, 4, 5, 6, 7, 8]) rejects(() => model.get_grid_spacing(id, new Float64Array(2)), 'BMIGridOperationError');
  model.get_grid_z(4, new Float64Array(2)); model.get_grid_z(6, new Float64Array(6));
});

test('empty point and edge-network topology has zero-length exact buffers', () => {
  const model = initialized();
  for (const id of [5, 6, 7]) {
    assert.equal(model.get_grid_face_count(id), 0);
    for (const field of ['face_nodes', 'face_edges', 'nodes_per_face', ...(id === 7 ? [] : ['edge_nodes'])]) {
      const dest = new Int32Array(0);
      assert.equal(model['get_grid_' + field](id, dest), dest);
      rejects(() => model['get_grid_' + field](id, new Int32Array(1)), 'BMIBufferError');
      rejects(() => model['get_grid_' + field](id, new Float64Array(0)), 'BMITypeError');
    }
  }
});

test('mixed ragged faces have valid IDs, connected boundaries and counter-clockwise winding', () => {
  const model = initialized();
  const nodes = model.get_grid_face_nodes(8, new Int32Array(11));
  const edges = model.get_grid_face_edges(8, new Int32Array(11));
  const sizes = model.get_grid_nodes_per_face(8, new Int32Array(3));
  const edgeNodes = model.get_grid_edge_nodes(8, new Int32Array(16));
  const x = model.get_grid_x(8, new Float64Array(6));
  const y = model.get_grid_y(8, new Float64Array(6));
  let offset = 0;
  for (const count of sizes) {
    let area = 0;
    for (let i = 0; i < count; i += 1) {
      const a = nodes[offset + i]; const b = nodes[offset + (i + 1) % count]; const edge = edges[offset + i];
      assert.ok(a >= 0 && a < 6 && edge >= 0 && edge < 8);
      assert.deepEqual(new Set([a, b]), new Set(edgeNodes.slice(edge * 2, edge * 2 + 2)));
      area += x[a] * y[b] - x[b] * y[a];
    }
    assert.ok(area > 0); offset += count;
  }
  assert.equal(offset, 11);
});

test('copy, pointer, full/indexed writes, overlap and duplicate order', () => {
  const model = initialized(); const name = 'unstructured_edges__flow_velocity';
  const pointer = model.get_value_ptr(name); const copy = new Float64Array(4);
  assert.equal(model.get_value(name, copy), copy); assert.notEqual(copy.buffer, pointer.buffer);
  copy[0] = 90; assert.equal(pointer[0], 2.1);
  pointer[0] = 10; model.get_value(name, copy); assert.equal(copy[0], 10);
  model.set_value(name, new Float64Array([0, 1, 2, 3])); assert.equal(model.get_value_ptr(name), pointer);
  model.set_value_at_indices(name, new Int32Array([3, 2, 1, 0]), pointer);
  assert.deepEqual([...pointer], [3, 2, 1, 0]);
  model.get_value_at_indices(name, pointer, new Int32Array([3, 2, 1, 0]));
  assert.deepEqual([...pointer], [0, 1, 2, 3]);
  model.set_value_at_indices(name, new Int32Array([0, 0]), new Float64Array([20, 30]));
  assert.equal(pointer[0], 30);
  model.get_value_at_indices(name, new Float64Array(0), new Int32Array(0));
  model.set_value_at_indices(name, new Int32Array(0), new Float64Array(0));
});

for (const bad of [[0], 0, new Float64Array([0]), new Int32Array([-1]), new Int32Array([4]), new Uint32Array([0])]) {
  test(`index contract rejects ${bad?.constructor?.name ?? typeof bad}: ${String(bad)}`, () => {
    const model = initialized(); const name = 'unstructured_edges__flow_velocity';
    const pointer = model.get_value_ptr(name); const before = pointer.slice();
    const dest = new Float64Array([7]);
    assert.throws(() => model.get_value_at_indices(name, dest, bad));
    assert.throws(() => model.set_value_at_indices(name, bad, dest));
    assert.deepEqual(pointer, before); assert.deepEqual([...dest], [7]);
  });
}

for (const [dtype, spec] of Object.entries(DTYPES)) {
  test(`primitive ${dtype} preserves precision and rejects implicit casts`, () => {
    const model = initialized(); const name = model.get_output_var_names().find(n => { const v = model.describeVariable(n); return v.grid === 0 && !v.evolving && v.dtype === dtype; });
    const pointer = model.get_value_ptr(name);
    assert.equal(model.get_var_itemsize(name), spec.ctor.BYTES_PER_ELEMENT);
    const values = spec.min === undefined ? [0, -0, Math.fround(1.0000001192092896), dtype === 'float64' ? Number.MAX_VALUE : 3.4028234663852886e38] : [spec.min, spec.max];
    for (const value of values) {
      const src = new spec.ctor([value]); const dest = new spec.ctor(1);
      model.set_value(name, src); assert.equal(model.get_value(name, dest), dest);
      assert.deepEqual(new Uint8Array(dest.buffer), new Uint8Array(src.buffer));
      model.set_value_at_indices(name, new Int32Array([0]), src);
      model.get_value_at_indices(name, dest, new Int32Array([0]));
      assert.deepEqual(new Uint8Array(dest.buffer), new Uint8Array(src.buffer));
      assert.equal(model.get_value_ptr(name), pointer);
    }
    rejects(() => model.set_value(name, dtype === 'float64' ? new Float32Array(1) : new Float64Array(1)), 'BMITypeError');
  });
}

test('UI conversions check integer overflow/fractions before TypedArray constructors can wrap', () => {
  for (const [text, dtype] of [['256', 'uint8'], ['-1', 'uint8'], ['128', 'int8'], ['1.2', 'int32'], ['2147483648', 'int32'], ['Infinity', 'float64'], ['3.5e38', 'float32'], ['18446744073709551616', 'uint64'], ['1.1', 'int64']]) {
    rejects(() => parseBuffer(text, dtype), 'BMITypeError');
  }
  assert.equal(parseBuffer('18446744073709551615', 'uint64')[0], 18446744073709551615n);
  assert.equal(parseBuffer('-9223372036854775808', 'int64')[0], -9223372036854775808n);
  assert.ok(Object.is(parseBuffer('-0', 'float64')[0], -0));
  assert.equal(parseBuffer('', 'float64').length, 0);
});

test('fixed contiguous subviews are allowed; DataView, subclasses and detached buffers fail', () => {
  const full = new Float64Array([1, 2, 3, 4]);
  assert.equal(buffer(full.subarray(1, 3), 'float64', 2, 'probe').length, 2);
  class PretendBuffer extends Float64Array {}
  rejects(() => buffer(new PretendBuffer(2), 'float64', 2, 'probe'), 'BMITypeError');
  const detached = new Float64Array(2); structuredClone(detached, { transfer: [detached.buffer] });
  rejects(() => buffer(detached, 'float64', 0, 'probe'), 'BMIBufferError');
  const resizable = new Float64Array(new ArrayBuffer(16, { maxByteLength: 32 }));
  rejects(() => buffer(resizable, 'float64', 2, 'probe'), 'BMIBufferError');
});

test('time/lifecycle is shared, validates before writes and never replaces storage', () => {
  const model = initialized(); const names = model.get_output_var_names();
  const pointers = names.map(n => model.get_value_ptr(n));
  const initial = pointers.map(v => v.slice());
  for (const bad of [-1, 3601, 10801, NaN, Infinity, '3600', true]) assert.throws(() => model.update_until(bad));
  assert.equal(model.get_current_time(), 0);
  pointers.forEach((v, i) => assert.deepEqual(v, initial[i]));
  model.update(); assert.equal(model.get_current_time(), 3600);
  pointers.forEach((v, i) => {
    assert.equal(v, model.get_value_ptr(names[i]));
    const evolving = model.describeVariable(names[i]).evolving;
    assert.deepEqual([...v], [...initial[i]].map(value => evolving ? value + model.describeVariable(names[i]).step_change : value));
  });
  model.update_until(10800); rejects(() => model.update(), 'BMILifecycleError');
  const held = model.get_value_ptr('uniform_2d__slope');
  model.finalize();
  for (const method of BMI_METHODS) rejects(() => model[method](), 'BMILifecycleError');
  const fresh = initialized(); held[0] = 999;
  assert.equal(fresh.get_value_ptr('uniform_2d__slope')[0], 0.0124);
});

test('fresh initialization rejects unsupported tokens/types without poisoning the new model', () => {
  const model = new BMI(); rejects(() => model.update(), 'BMILifecycleError');
  for (const token of ['scalar', 'uniform_2d', 'missing', [], {}, null, true]) rejects(() => model.initialize(token), 'BMIIndexError');
  model.initialize(''); assert.equal(model.scenarioKey, 'all_grids');
  rejects(() => model.initialize('all_grids'), 'BMILifecycleError');
  for (const id of [-1, 9, 1.5, '1', true, NaN]) rejects(() => model.get_grid_type(id), 'BMIIndexError');
  for (const name of ['__proto__', 'missing', [], 1, null]) rejects(() => model.get_var_grid(name), 'BMIIndexError');
});

test('rendering geometry preserves true coordinates, shape ordering and topology distinction', () => {
  const model = initialized();
  const uniform = geometryNodes(model.describeGrid(2));
  assert.equal(uniform.length, 24);
  assert.deepEqual(uniform[18], { index: 18, x: 110, y: 12, z: 7 });
  const rect = geometryNodes(model.describeGrid(4));
  assert.deepEqual(rect[18], { index: 18, x: 107, y: 11, z: 7 });
  assert.equal(geometryLinks(model.describeGrid(5)).edges.length, 0);
  assert.equal(geometryLinks(model.describeGrid(8)).faces.length, 3);
  assert.ok(geometryLinks(model.describeGrid(1)).edges.length > 0);
  rejects(() => model.get_grid_edge_count(1), 'BMIGridOperationError');
});

for (const key of Object.keys(SCENARIOS)) {
  test(`scenario ${key} changes geometry without changing ranks, counts or connectivity`, () => {
    const model = initialized(key); const data = scenarioData(key); const base = scenarioData('all_grids');
    assert.equal(model.get_output_item_count(), 21);
    data.grids.forEach((grid, i) => {
      assert.equal(grid.rank, base.grids[i].rank);
      assert.deepEqual(grid.shape, base.grids[i].shape);
      assert.deepEqual(grid.edge_nodes, base.grids[i].edge_nodes);
      assert.deepEqual(grid.face_nodes, base.grids[i].face_nodes);
    });
    const expectedX = key === 'stretched_domain' ? [200, 204, 214, 230] : key === 'shifted_domain' ? [-20, -18, -13, -5] : [100, 102, 107, 115];
    assert.deepEqual([...model.get_grid_x(3, new Float64Array(4))], expectedX);
    if (key === 'shifted_domain') assert.deepEqual([...model.get_grid_origin(1, new Float64Array(2))], [-10, -20]);
  });
}

test('method controls use variable cardinality and the API indexed-setter argument order', () => {
  const model = initialized(); const grid = model.describeGrid(8); const variable = model.describeVariable('unstructured_mixed__precipitation_rate');
  assert.equal(operationSpec('get_value', grid, variable).count, 3);
  assert.equal(operationSpec('get_value_at_indices', grid, variable, 2).count, 2);
  assert.match(operationSpec('set_value_at_indices', grid, variable).signature, /inds, src/);
  assert.equal(operationSpec('get_grid_shape', grid, variable).applicable, false);
  assert.equal(operationSpec('get_grid_face_nodes', grid, variable).count, 11);
});

for (const bad of [[1, 2, 3, 4], 9, new Float32Array(4), new Int32Array(4), new Float64Array(3), new Float64Array(5), new DataView(new ArrayBuffer(32))]) {
  test(`full value access refuses ${bad?.constructor?.name}: ${ArrayBuffer.isView(bad) ? bad.byteLength : 'non-buffer'}`, () => {
    const model = initialized(); const name = 'unstructured_edges__flow_velocity';
    const pointer = model.get_value_ptr(name); const before = pointer.slice();
    const destinationBefore = bad instanceof Float64Array || Array.isArray(bad) ? [...bad] : null;
    assert.throws(() => model.set_value(name, bad));
    assert.throws(() => model.get_value(name, bad));
    assert.deepEqual(pointer, before);
    if (destinationBefore) assert.deepEqual([...bad], destinationBefore);
  });
}

test('a same-time update is a bit-preserving no-op, including signed zero', () => {
  const model = initialized();
  model.set_value('scalar__velocity', new Float64Array([-0]));
  model.update_until(0);
  assert.ok(Object.is(model.get_value_ptr('scalar__velocity')[0], -0));
  rejects(() => buffer(Object.create(Float64Array.prototype), 'float64', 1, 'probe'), 'BMITypeError');
});

for (const scenario of Object.keys(SCENARIOS)) {
  test(`hydrological defaults remain plausible through end time in ${scenario}`, () => {
    const model = initialized(scenario);
    const cases = [
      ['uniform_3d__soil_temp', 'degC', 12.2, 14.8, 0.1],
      ['rectilinear_3d__saturation', '1', 0.45, 0.85, 0.01],
      ['points_2d__snow_depth', 'm', 0.1, 0.32, -0.002],
      ['rectilinear_2d__precip_rate', 'mm h-1', 1.2, 4.0, 0.25],
    ];
    const slope = model.get_value_ptr('uniform_2d__slope').slice();
    for (let step = 0; step <= 3; step += 1) {
      model.update_until(step * 3600);
      for (const [name, units, low, high, change] of cases) {
        const values = model.get_value_ptr(name);
        assert.equal(model.get_var_units(name), units);
        assert.ok(Math.abs(Math.min(...values) - (low + step * change)) < 1e-12, name);
        assert.ok(Math.abs(Math.max(...values) - (high + step * change)) < 1e-12, name);
      }
    }
    assert.deepEqual(model.get_value_ptr('uniform_2d__slope'), slope);
    assert.equal(model.get_value_ptr('scalar__scaled_temp')[0] / 100, 23.45);
    assert.equal(model.get_var_units('scalar__scaled_temp'), '0.01 degC');
    assert.equal(model.get_value_ptr('scalar__flow_direction_code')[0], 64);
  });
}
