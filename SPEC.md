# SPEC.md: BMI Explorer

**Project:** BMI Explorer  
**Status:** Implementation specification  
**Language:** Python 3.11+  
**Required dependency:** NumPy  
**Primary interface:** CSDMS Basic Model Interface (BMI) Python specification  
**Primary source:** https://github.com/csdms/bmi-python/blob/master/src/bmipy/bmi.py  
**Normative explanatory sources:** https://bmi.csdms.io/en/stable/model_grids.html and https://bmi.csdms.io/en/stable/bmi.grid_funcs.html

## 1. Purpose

BMI Explorer is a small, self-contained, interactive teaching and experimentation application. Running it opens a Python shell implemented with the standard library's `code.InteractiveConsole`, preloaded with **one real, stateful BMI implementation** backed by deterministic, inspectable NumPy arrays. One built-in scenario, `all_grids`, owns all required grids simultaneously on the same `bmi` object; comparing grid types must never require switching scenarios or model instances.

Its purpose is to make the entire BMI contract concrete: grid identity, geometry, topology, variable locations, buffer allocation, C-style value retrieval and insertion, type and byte counts, memory ownership, index ordering, and model lifecycle. Users should discover the rules by calling BMI functions themselves, including operations that intentionally fail with explanatory errors.

The application must never quietly allow an operation merely because Python or NumPy can coerce, reshape, broadcast, duck-type, or allocate an object in a way that would hide a violation of the equivalent typed, caller-allocated C++ BMI call.

**Educational objective:** After experimenting, a user should be able to design and consume `scalar`, `uniform_rectilinear`, `unstructured`, `points`, and `rectilinear` BMI grids on one model, compare representative ranks 0 through 3, distinguish node/edge/face values, allocate correct output buffers, and explain what is guaranteed by BMI versus what is a model- or Explorer-specific convention.

**Non-goals:** Running real scientific solvers, loading external datasets, GIS rendering, arbitrary Python-to-C++ ABI simulation, guaranteeing safety of invalid raw C++ pointers, supporting unsupported ranks or four-dimensional geometry, and auto-correcting malformed user calls. The console core needs no web server or database. Per the later playground usability request, prompt_toolkit and Pygments provide terminal editing while code.InteractiveConsole retains Python execution semantics. The separately requested static web companion is defined in section 14.

## 2. Sources and precedence

1. The `bmipy.Bmi` abstract interface at the linked repository defines required Python method names, signatures, and return conventions.
2. Official CSDMS BMI 2.0 grid and function documentation defines grid families, coordinate conventions, topology buffers, and C++ equivalents.
3. An optional C++ contract reference may be consulted for parity. Keep Python snake_case methods as the public BMI API. Do not invent C++ features that are not defined by the BMI C++ interface.
4. Where source descriptions are ambiguous, inconsistent, or leave behavior undefined, **document an Explorer policy**, attach an explanatory note, and test it. Do not present a policy as a universal BMI mandate.
5. The Python specification sometimes describes NumPy array arguments with flexible typing, while C++ exposes typed caller-owned memory (`void*`, `int*`, `double*`). For teaching purposes enforce the tighter, explicit buffer contract in the Explorer fixtures. Cross-language strictness is about **observable valid calls**, not literal C++ memory safety or implementation internals.

Each operation's help/inspection metadata must display its provenance: `BMI REQUIRED`, `GRID-TYPE APPLICABILITY`, `C++ PARITY`, or `EXPLORER POLICY`. The project must maintain a `docs/decisions.md` register for ambiguous cases.

## 3. Launch and interactive user experience

Installable package name: `bmi-explorer` (import package `bmi_explorer`). Provide both:

```sh
python -m bmi_explorer
bmi-explorer
```

Running either command opens a persistent, stateful `code.InteractiveConsole` session with a brief banner, the `all_grids` scenario's grid inventory (IDs, labels, types, ranks, and variable names), and example commands. No manual initialization is required. Provide `--list` to display that inventory, `--tour NAME`, `--no-banner`, and `--strict` (strict is the default and cannot be silently disabled; `--strict` merely makes intent explicit). Retain `--scenario NAME` only as a compatibility selector accepting `all_grids`, which is also the default; other names fail clearly. A `--relaxed` mode is explicitly **out of scope**.

Prepopulate console locals:

- `np`: the actual NumPy module, for user-side buffer creation.
- `bmi`: the already-initialized BMI implementation owning every grid in `all_grids`.
- `explorer`: non-BMI teaching and grid-discovery utility, clearly separate from `bmi`.
- `scenarios`: read-only compatibility registry containing only `all_grids` and its description.
- `help_bmi`: helper for methods, examples, constraints, and expected errors.

Expected interactions:

```python
>>> explorer.list()
>>> g = bmi.get_var_grid("uniform_2d__slope")
>>> bmi.get_grid_type(g)
'uniform_rectilinear'
>>> rank = bmi.get_grid_rank(g)
>>> shape = np.empty(rank, dtype=np.int32)
>>> bmi.get_grid_shape(g, shape)
array([3, 4], dtype=int32)
>>> r = bmi.get_var_grid("rectilinear_2d__precip_rate")
>>> bmi.get_grid_type(r)
'rectilinear'
>>> explorer.try_call("get_grid_spacing", r, np.empty(bmi.get_grid_rank(r), dtype=np.float64))
>>> explorer.describe("uniform_2d__slope")
>>> explorer.reset()
```

Examples resolve grid IDs through variable names rather than assuming a global meaning for ID zero. The names above are illustrative fixture labels, not certified CSDMS Standard Names. `explorer.list()` lists every grid in the current model and its variables; it does not select or instantiate a model. BMI itself has no grid-enumeration method: users can also discover IDs by collecting `get_var_grid(name)` over the input/output variable names.

The console must support normal Python expressions, multiline statements, exceptions, `help()`, history when the runtime offers it, and clean exit via `exit()`/EOF. Do not intercept Python input with a custom language or `eval` parser. An uncaught error prints a readable exception and leaves the REPL usable. Avoid global monkeypatching. Interactive terminals provide syntax highlighting, Tab completion, session history/search and bracket matching; redirected input stays plain. Print help into scrollback without an external pager. Startup guidance uses wrapped grid/variable rows and runnable examples; show print(...) when a teaching helper returns multiline text.

Use `code.InteractiveConsole(interact)` directly or a thin subclass to improve exception presentation. The user is running arbitrary Python in their local process; **do not claim this is a secure sandbox**.

`explorer.try_call(method_name, *args)` invokes exactly the named BMI method, prints its returned result or error plus a plain-English explanation, and does not automatically repair the arguments. `explorer.describe(name_or_grid)`, `explorer.methods(grid_id)`, `explorer.example(method, grid_id=...)`, `explorer.compare(a, b)` (two grid IDs on the current model), and `explorer.tour(name)` are optional educational helpers **outside** the BMI surface. Provide `explorer.reset()` to recreate the complete scenario and restore all grids, variables, and time together. Scenario switching is not part of the learning workflow; if `explorer.use()` is retained for compatibility it accepts only `all_grids`. Keep the raw `bmi` object easy to access.

## 4. Grid taxonomy and coverage

Require **these five exact grid-type strings**, all present on the same model:

| Type | Concept | Typical grid rank | Key geometry API |
|---|---|---:|---|
| `scalar` | Single non-spatial value | 0 | Rank/size/type; no axes |
| `points` | Set of point locations without mesh connectivity | 2, 3 | Per-node coordinates on active axes |
| `uniform_rectilinear` | Structured orthogonal grid with constant spacing | 2, 3 | Shape, spacing, origin |
| `rectilinear` | Structured orthogonal grid with varying spacing | 2, 3 | Shape and coordinate arrays per axis |
| `unstructured` | Explicit topology, potentially mixed face sizes | 1, 2 | Coordinates, counts, edge/face connectivity |

Use one scalar grid and two grids of different ranks for each other required type: nine grids total. Scalar remains rank 0; do not invent a second scalar rank. `vector` and `structured_quadrilateral` are outside this release's required coverage; explain them only as context where useful.

**Important distinction:** Grid rank is the grid's number of geometric dimensions. A variable's NumPy rank, a value's number of components, the count of points, and the topological dimension are separate concepts. Especially for `points`, embedded surfaces, and unstructured grids, document the selected interpretation per fixture rather than asserting that rank equals the number of nodes or NumPy dimensions.

For each type, provide valid and invalid operations in the method applicability catalog. All abstract BMI methods **must exist** on all implementation objects, but grid-inapplicable methods must raise a controlled `NotImplementedError` (or dedicated subclass) identifying the grid type and why the method is not applicable. Do not return arbitrary empty arrays, fabricate spacing, or silently use zeros.

### 4.1 Single deterministic scenario and grid inventory

`all_grids` is the sole scenario. The following labels identify grids within its one model, not independently selectable scenarios. Each grid has a distinct, stable integer ID within the scenario and at least one discoverable variable mapped to it by `get_var_grid`. Reinitialization/reset reproduces the same mapping.

| Grid label | Type | Rank | Geometry / learning objective |
|---|---|---:|---|
| `scalar` | `scalar` | 0 | Exactly one logical value; storage without spatial axes |
| `uniform_2d` | `uniform_rectilinear` | 2 | Three rows by four columns; shape `[3, 4]` |
| `uniform_3d` | `uniform_rectilinear` | 3 | Two layers by three rows by four columns; shape `[2, 3, 4]` |
| `rectilinear_2d` | `rectilinear` | 2 | Nonuniform x/y axes; shape `[3, 4]` |
| `rectilinear_3d` | `rectilinear` | 3 | Nonuniform x/y/z axes; shape `[2, 3, 4]` |
| `points_2d` | `points` | 2 | Six scattered x/y nodes, no mesh connectivity |
| `points_3d` | `points` | 3 | Six scattered x/y/z nodes, no mesh connectivity |
| `unstructured_edges` | `unstructured` | 1 | Four x-axis nodes and three connected edges, no faces |
| `unstructured_mixed` | `unstructured` | 2 | Six nodes, eight edges, three mixed triangle/quadrilateral faces |

Every grid exposes a node-valued float64 hydrological quantity, with a meaningful
variable name, matching units and plausible initial values. Soil temperature is
in degrees Celsius, precipitation rate in mm/hour, saturation a fraction, and
snow/water depth in metres. Ten additional scalar attributes cover the required
primitive widths using meaningful quantities/codes/counts. The mixed mesh also
exposes signed edge discharge and face precipitation rate. The full inventory,
units, example values and hourly changes are specified in
`docs/business-configuration.md` and immutable fixture descriptors. These are
synthetic teaching samples, not observed datasets or a calibrated solver. At
least two variables share a grid ID, including different mesh locations.

Keep shared-grid, multiple-grid, location, and time lessons within `all_grids`. Mutating one variable must leave other variables and grid descriptors unchanged; only documented update rules change other values. All grids share one lifecycle and one time clock. Comparisons must query both grids on the same initialized object without implicit reset, model replacement, or state loss.

No fixture should rely on unspecified random values. Give every grid a compact diagram/text legend, explicit expected coordinate/topology/value arrays, and a copyable 2–5-call demonstration. The applicability catalog and comparisons must show type, rank, size, coordinate-buffer lengths, topology counts where applicable, value-buffer lengths/bytes, and at least one method that succeeds on one grid and fails on another. Include comparisons between both ranks of each non-scalar type. Additional geometry variants, if added later, belong to this scenario and require an explicit scope revision rather than new scenario names.

### 4.2 Canonical numeric examples

**Uniform 2D:** Shape `[3, 4]`, spacing `[2.0, 5.0]`, origin `[10.0, 100.0]`, node count `12`. First node is `(x=100, y=10)`; last is `(x=115, y=14)` under the explicit row-major convention. `get_grid_shape` returns **node** counts, not the two-by-three count of quadrilateral cells. A node-valued variable has 12 values; a face-valued variable can have 6 values if faces are explicitly represented and supported by the fixture. Don't infer its storage count from `get_grid_size()`.

**Rectilinear 2D:** Shape `[3, 4]`; x `[100., 102., 107., 115.]`; y `[10., 11., 14.]`. `get_grid_x` returns 4 values; `get_grid_y` returns 3. `get_grid_spacing` must fail because these axes do not have a single spacing; `get_grid_origin` must fail in the canonical API applicability policy, even though the first coordinates could be used to calculate an origin outside BMI.

**Points 2D versus rectilinear 2D:** The point grid has six nodes, so both `get_grid_x` and `get_grid_y` write six per-node coordinates. The rectilinear grid has 12 nodes but writes four x-axis values and three y-axis values. Points have neither structured shape nor uniform spacing; those calls fail without changing the destination.

**Unstructured mixed faces:** Use six nodes, eight edges, and three faces, with the official documented topology example when practical. Expected `nodes_per_face=[4,4,3]`, `len(edge_nodes)=16`, and `len(face_edges)=len(face_nodes)=11`. Include an exact documented connectivity fixture and assert its node/edge IDs and winding. Show how to reconstruct face slices by cumulative `nodes_per_face` offsets; arbitrary `reshape(nfaces, 4)` is invalid.

**Scalar:** `get_grid_rank(grid_id)==0`, `get_grid_size(grid_id)==1`, `get_var_itemsize` equals the chosen type's byte width, and `get_var_nbytes` equals that itemsize. Scalar representation is a fixed single-element NumPy storage buffer for ABI teaching. `get_value`/`set_value` require an exact one-element typed array under the Explorer's strict policy; `get_value_at_indices` accepts only valid flat index `0`. Empty `shape`, `spacing`, or `origin` outputs are **not** advertised as meaningful scalar geometry operations; requests for non-applicable geometry error explicitly. Record that this one-element buffer is an Explorer policy to model C++ pointer semantics, not a universal Python scalar representation requirement.

## 5. Geometry and topology contract

### 5.1 Coordinate ordering

Use the official BMI **ij/indexing order** for shape, origin, spacing and structured array values:

- 1D: `[nx]`, `[dx]`, `[x0]`.
- 2D: `[ny, nx]`, `[dy, dx]`, `[y0, x0]`.
- 3D: `[nz, ny, nx]`, `[dz, dy, dx]`, `[z0, y0, x0]`.

For structured fixtures, choose C-contiguous arrays and document `C`-order flattening, with the last axis varying fastest. `inds` in indexed value operations are **flat, zero-based element indices** into the variable's value buffer, not coordinate tuples. Multidimensional Python tuples, slices, masks, `np.ravel_multi_index` results passed in the wrong dtype, or list-of-list indices must not be silently accepted by the BMI methods. Users can calculate valid flat indices themselves using NumPy and supply them in properly typed buffers.

Show the mapping for a 3x4 node array: `[[0,1,2,3],[4,5,6,7],[8,9,10,11]]`; row 1, column 2 corresponds to flat index 6. Explain that a 3D grid's shape is geometry metadata and that coordinate names `x/y/z` refer to physical axes even though shape is stored in reverse order.

### 5.2 Which methods belong to which grid

- All grids: `get_grid_type`, `get_grid_rank`, `get_grid_size`.
- Uniform rectilinear: `get_grid_shape`, `get_grid_spacing`, `get_grid_origin`; coordinate arrays can be derived externally, but should not be silently exposed through non-applicable BMI methods.
- Rectilinear: `get_grid_shape`, relevant `get_grid_x/y/z` axis vectors.
- Unstructured: relevant `get_grid_x/y/z`, node/edge/face counts, and supported topology routines; describe zero-count topology and operations in the applicability catalog. The exact behavior of empty topology arrays must be explicit.
- `scalar`, `points`: use documented fixtures and CSDMS's special-case unstructured-family semantics, not pretend all unstructured connectivity calls are useful for each case.

If a geometric method is not applicable, no buffer mutation is allowed. Unavailable operations must fail before any destination writes. For a missing coordinate axis, `get_grid_z` on a 2D grid is not an invitation to return an all-zero z array.

### 5.3 Topology

Use flat, zero-based integer connectivity buffers:

- `get_grid_node_count`: number of grid nodes.
- `get_grid_edge_count`: number of edges.
- `get_grid_face_count`: number of faces.
- `get_grid_edge_nodes`: exactly `2 * edge_count` integer entries, ordered tail/head per edge.
- `get_grid_nodes_per_face`: exactly `face_count` integer entries.
- `get_grid_face_nodes`: exactly `sum(nodes_per_face)` integer entries, grouped by face, counter-clockwise for 2D planar faces.
- `get_grid_face_edges`: exactly `sum(nodes_per_face)` integer entries, grouped by face.

Validate that referenced node and edge IDs are in range, all face boundaries are consistent, and topology arrays and cardinalities agree. Provide human-readable `explorer.topology(grid_id)` showing each face's node IDs and edge IDs.

**3D caveat:** BMI's node/edge/face API does not provide a general volume/cell connectivity interface. A rank-3 spatial grid or 3D coordinates must not be marketed as proof that arbitrary 3D volumetric polyhedra are fully describable through BMI topology calls. Include a specific illustration of this limit.

## 6. Variables, locations, types, and memory

### 6.1 Fixture variable descriptors

Every variable has an immutable descriptor containing name, grid ID, location, dtype, units, read/write exposure (where relevant), expected value count, and initial values. Store current values in separate mutable, typed, C-contiguous NumPy buffers. Never expose descriptor mutation as BMI state mutation.

Names in the declared input/output name collections must be deterministic. Use meaningful CSDMS-style long names where possible and identify illustrative nonstandard names as fixture labels rather than falsely certifying them as official CSDMS Standard Names.

### 6.2 Value locations

`get_var_location(name)` must return only `node`, `edge`, or `face`. Do not introduce `cell`, `grid`, `scalar`, or `volume` as extra strings. Show location as an association between **each variable** and an element type, not as a property of the variable's rank or dtype.

For the canonical mixed unstructured mesh, a node variable has `node_count` values, an edge variable has `edge_count` values, and a face variable has `face_count` values. Use this mesh for the required node/edge/face comparison. Uniform and rectilinear grids need only node-valued variables in this release. Where the BMI API does not standardize a cardinality mapping for a particular 3D feature or vector-valued field, make it a documented fixture policy rather than introducing an extra required grid.

A scalar uses location `node` by explicit Explorer convention, representing its single logical element; do not invent a fourth location category. Include examples where two variables share a grid but have different locations.

### 6.3 Primitive types

Use fixed-width NumPy numeric dtypes to represent the kinds of fundamental C/C++ scalar values the fixtures claim to expose: at least `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64`, `float32`, and `float64`, with signed/unsigned byte-size calculations tested. Optional platform-dependent `long double` should be excluded until its cross-platform ABI behavior can be explained accurately.

`get_var_type()` returns a declared primitive type label that is consistent with the documented C++ BMI vocabulary for that fixture; `get_var_itemsize()` returns NumPy dtype itemsize in bytes; `get_var_nbytes()` returns the actual exposed variable buffer byte size. No variable may claim a compound type such as `vector<vector<int>>` as its BMI primitive element type. Vectors and multidimensional arrays are **collections of primitive elements**.

Type spellings are not uniformly standardized between programming languages; keep a `docs/type-mapping.md` table distinguishing the declared BMI name, NumPy dtype, and C++ equivalent. A type spelling accepted by one model must not be advertised as universally required across all models. Do not silently convert an integer to a float, a float64 array to float32, signed to unsigned, or a Python sequence to a typed buffer.

### 6.4 Access and pointer semantics

Implement all five BMI value methods with strict input checking:

| Method | Contract |
|---|---|
| `get_value(name, dest)` | Copy values into an existing destination buffer of exactly correct dtype and element count; return the same `dest` array object as specified by the linked Python interface |
| `get_value_ptr(name)` | Return a live, writable view/reference of the model-owned storage, not a copy; explain that validity depends on the model lifecycle |
| `get_value_at_indices(name, dest, inds)` | Copy precisely one value per zero-based flat index into preallocated `dest`; require exactly matching lengths |
| `set_value(name, src)` | Copy a full typed source buffer into model-owned storage; never replace the storage object silently or broadcast a scalar |
| `set_value_at_indices(name, inds, src)` | Set one value per flat index, with exact dtype and lengths; reject out-of-range indices |

The indexed access methods operate on the **variable value buffer**, not unconditionally on `get_grid_size()`. In a mixed unstructured mesh, face-value index `2` is valid when there are three faces, even if the grid has six nodes; face-value index `3` is invalid.

Require actual `np.ndarray` buffers (not Python lists, tuples, numbers, memoryviews, or array-like duck types), native-compatible dtype/byte-order, writeable destinations, C-contiguity for all buffers, and exact expected sizes. For teaching, favor one-dimensional contiguous buffers in the public value methods even when internal structured arrays can be reshaped for presentation. Reject `dtype=object`, mismatched numeric types, noncontiguous views, zero-dimensional NumPy scalar objects, negative indices, bool indices, masks, tuples, slice objects, and broadcasting. Guard against NumPy's permissive assignment and aliasing; stage an input if required to preserve deterministic behavior when `src` overlaps destination storage.

**Indexed integer-width policy:** Use `np.int32` as the fixture's C++-`int` representative, with a platform check verifying the chosen C++ equivalent is 32-bit in the documented teaching ABI. C++ `int` is not guaranteed to be 32-bit by the language standard. Do not claim `np.int_` and `np.int32` are universally identical, or rely on them being identical on all platforms. Explain the distinction.

**Pointers and mutation:** `get_value_ptr()` returns an ndarray referring to backing storage. Mutating it should immediately affect `get_value()`; mutating a copy from `get_value()` must not. `set_value()` must update in place, preserving earlier pointer views. `finalize()` invalidates all operations on the BMI object. Python cannot revoke a previously returned ndarray reference, so the Explorer must explain that such retained arrays can survive finalization while analogous raw C++ pointer use may become invalid/undefined. It should never falsely promise identical lifetime safety.

### 6.5 Validation and diagnostics

Create a small, clearly named error hierarchy, e.g., `BMIExplorerError`, `BMITypeError`, `BMIBufferError`, `BMIIndexError`, `BMIGridOperationError`, and `BMILifecycleError`. Derive from appropriate built-in `TypeError`, `ValueError`, `IndexError`, and `NotImplementedError` where useful. Exceptions must identify method, variable/grid, received type/shape/dtype, expected type/size, reason, and a concrete valid call. Never mutate model state or destination buffers on failed validation. All validation precedes writes.

Example error text:

```text
BMIBufferError: set_value('surface_water__depth') expected a C-contiguous
numpy.ndarray(dtype=float64, size=12); received list with 12 elements.
Python could coerce this input, but the corresponding C++ BMI call consumes
a typed pointer to an existing buffer. Try np.array(values, dtype=np.float64).
```

Note the last line is educational, not automatic coercion. The messages should also distinguish **not supported for this grid type** from **valid method with invalid arguments** and from **outside the BMI standard**.

## 7. Model lifecycle and time

Implement `initialize(config_file)`, `update()`, `update_until(time)`, and `finalize()`, even though the console launches an initialized default instance. `initialize` must reproducibly construct every grid and variable in `all_grids` together. Use the documented built-in token `all_grids` (also selected by the default empty configuration); retain the BMI signature with no silent arbitrary extra arguments. Other scenario tokens must fail clearly.

Provide a deterministic time fixture with start `0.0`, current `0.0`, step `3600.0`, and end `10800.0`, time units `s`. Values at `t=0` must be explicitly initialized and readable; `update()` advances to `t=3600` and updates selected example values according to documented quantity-specific hourly changes. Shipped saturation remains in [0,1], temperatures stay plausible in their stated units, and depths remain nonnegative through end time. Slope and scalar attributes are static; user writes are not physically clamped. `update_until()` rejects times earlier than current time, beyond end time, non-finite values, and unsupported fractional targets if the fixture only supports integral timesteps. Do not claim all BMI models prohibit fractional steps; this is the fixture's policy.

`initialize` twice, `update` before initialization, operations after `finalize`, and pointer reuse across lifecycle transitions all get dedicated lessons. State resets must not accidentally preserve invalid references as if they were safe pointers.

## 8. Interactive teaching content

Help must be available both as `help_bmi('get_grid_shape')` and via `explorer.describe(...)`. Every BMI method should have a compact entry showing: signature, valid grid categories, exact buffer dtype and length formula, sample call, expected result, common mistaken call, expected exception, C++ equivalent, and relevant standard/convention citations.

Tours must be executable interactively, pause between examples **only on explicit user action**, and never auto-run long simulations. Suggested tours:

1. **Scalar is not a one-cell raster:** scalar grid, rank 0, one-element buffer, type and nbytes, indexed `0`, no spacing.
2. **Grid rank vs variable shape:** spatial rank, node shape, face counts, NumPy shape, and vector component count.
3. **Uniform versus nonuniform:** why `[dy, dx]` exists for uniform but not general rectilinear geometry.
4. **Axes versus point coordinates:** rectilinear axis vectors versus per-node point x/y/z arrays, including different ranks on the same object.
5. **Unstructured anatomy:** nodes, edges, faces, orientation, ragged face-node connectivity.
6. **Node, edge, or face:** same mesh, different variable lengths and valid indices.
7. **Read vs pointer:** copying, views, in-place writes, invalidation concerns.
8. **Strict C++ behavior:** wrong buffer dtype, wrong length, list input, implicit broadcasting, shape mismatch, index errors.
9. **Time and lifecycle:** initial state, update, exact time target, finalization.
10. **The boundary of BMI:** nonstandard properties, units, vectors/components, 3D volumes, and what interfaces cannot reveal.

Each tour must contain at least one valid and one deliberately invalid probe, show expected results before user interaction if requested (`explorer.example`), and explain the failure without shaming the learner.

## 9. Architecture

Suggested package layout:

```text
SPEC.md
README.md
pyproject.toml
src/bmi_explorer/
    __init__.py
    __main__.py
    cli.py
    console.py
    model.py
    descriptors.py
    grids.py
    variables.py
    validation.py
    errors.py
    explorer.py
    fixtures.py
    lessons.py
    reference.py
    py.typed
tests/
    test_bmi_contract.py
    test_grid_types.py
    test_value_buffers.py
    test_scalar.py
    test_topology.py
    test_lifecycle.py
    test_console.py
    test_negative_cases.py
docs/
    decisions.md
    type-mapping.md
    grid-matrix.md
```

Use typed frozen dataclasses or equivalent for grid/variable descriptors, with mutable model-owned storage separated from metadata. A core class must concretely implement/subclass `bmipy.Bmi`, if that package is installed. To minimize dependencies, a local protocol-compatible implementation may provide the same surface when `bmipy` is not installed; the distinction must be documented and conformance tested against the linked abstract interface. Because the requested specification is the authority, prefer depending on `bmipy` if its packaging and Python compatibility are suitable. No code should import optional dependencies on startup unless installed.

Prefer dispatch tables or polymorphic grid descriptor classes for type-specific behavior, with one central validator and one central applicability registry. One model owns a grid-ID-to-descriptor mapping and a variable-name-to-descriptor/storage mapping; each variable resolves its grid ID through those mappings. Do not represent grids as separate BMI instances or build a model wrapper that swaps the active grid before each call. Avoid scattered magic grid-type string tests and unvalidated NumPy arrays from an internal adapter. Keep operations readily testable independently of the REPL.

Keep NumPy as the only required third-party runtime dependency unless adopting `bmipy` as the minimal reference-interface dependency; `pytest` can be a development dependency. No pandas, xarray, GIS toolkit, web framework, plotting library, or database required. Provide optional extension points but do not implement them for version 1.

**Code documentation convention:** Use comprehensive type hints, class/module/function docstrings and explanatory comments. In every developer-authored module/class/function docstring, include a conspicuous `TODO: AI-generated implementation; human review and rewrite required.` marker, per project coding-review policy. Do not let this marker substitute for useful documentation.

## 10. Compatibility matrix and conformance suite

Maintain machine-readable operation metadata and a generated human-readable matrix, with rows for all 41 BMI methods from the linked Python ABC (verify the count programmatically rather than hardcoding it). Matrix columns: applicability by grid type, output dtype, output-size rule, return convention, C++-parity restrictions, expected error, and fixture exercising the method.

The tests must include:

- Concrete model implements every abstract method and agrees with the installed/reference `bmipy.Bmi` signature set.
- Each grid type and planned rank has at least one successful test and one intentional failure.
- A single initialized `all_grids` model exposes exactly the nine planned grids and all five required types, with the ranks from section 4.1. Every grid is reachable through at least one input/output variable, IDs are distinct across grids, and variables sharing a grid return the same ID.
- Interleaved queries across types/ranks on that same object match exact expected results without reinitialization or replacement. A write affects only its target variable; failed calls on one grid preserve every other grid and variable. Reset restores the entire inventory, initial values, ID mapping, and shared clock.
- Every method's unsupported-grid invocation raises the expected exception and does not mutate a destination.
- Each grid size/shape and value byte-count agrees with its fixture, with location-specific value counts.
- Uniform/rectilinear/points coordinate lengths and ij ordering where applicable, including 3D ordering, are exact.
- All unstructured connectivity IDs, lengths, face offsets, winding, and node-edge-face relationships are valid.
- Strict dtype, byte order, contiguity, writeability, shape/length, and index validation runs before mutation.
- Integer and float range/precision cases are deterministic; wrong types do not silently cast.
- `get_value` returns exactly the passed `dest` object, writes into it, and makes a copy; `get_value_ptr` aliases backing state; `set_value` preserves storage identity.
- Scalar read/write (full and indexed) works, while invalid scalar geometry fails.
- Time/lifecycle transitions and attempted operations on finalized objects fail as specified.
- No Python list, tuple, array duck type, implicit reshape, broadcasting, or scalar coercion bypasses C++-parity rules.
- Console launch succeeds under `python -m bmi_explorer`, normal errors are recoverable, and reset restores fixture state.
- The explanatory `help_bmi` entries cover every method and cite BMI requirements separately from Explorer choices.

Use parametrized positive/negative tests over the operation registry rather than duplicating hundreds of manual assertions. Include a smoke script of console input/output that developers can compare literally. CI should run against supported Python/NumPy combinations on Linux, Windows, and macOS. Document any platform-specific `int`/`long` ABI assumptions instead of hiding them.

## 11. Acceptance criteria

The deliverable is acceptable when a user can launch the interpreter with one command into the sole `all_grids` scenario, discover all nine grids across the five required types on the same `bmi` object, compare both ranks of each non-scalar type without switching models, call **every** BMI method, inspect values and topology, reproduce all documented valid results, and receive informative failures for invalid calls. All grids must coexist; a collection of separate single-grid scenarios does not satisfy this requirement.

Success specifically means a user can independently answer:

- Why does a scalar have grid rank 0 but still consume memory?
- What do shape, spacing, and origin mean in 1D, 2D, 3D, and why are they not available everywhere?
- Why are x/y coordinate lengths 4 and 3 on a 3x4 rectilinear grid, but both 6 on a six-node point grid?
- How can one BMI object expose a rank-0 scalar alongside different ranks of uniform, rectilinear, point, and unstructured grids, and how do variable names identify those grids?
- Why are the 6 node values, 8 edge values, and 3 face values of a single mesh all legitimate despite different lengths?
- What is the difference between rank, grid type, variable primitive type, components, variable location, and buffer shape?
- Why do `get_value` and `get_value_ptr` behave differently after a mutation?
- Why does a Python list, broadcast scalar, wrong dtype, or Python slice fail even though NumPy can normally handle it?
- How are flat indices mapped to structured nodes or unstructured elements?
- Which apparently convenient operations are outside the BMI contract?
- What can and cannot be inferred about a 3D unstructured volume from BMI topology?

A static document with examples alone is **not** sufficient. The executable fixtures, strict behavior, discoverability, and tests are all core features.

## 12. Implementation order

**Phase 1:** Pin/reference the BMI API, implement metadata registry, error classes, multi-grid model ownership, scalar and uniform 2D grids together in `all_grids`, preallocated value buffers, and `code.InteractiveConsole` entrypoint. Migrate the earlier separate-scenario implementation into this single inventory; it is an incomplete starting point, not the final scenario design.

**Phase 2:** Add uniform 3D and rectilinear 2D/3D grids to the same object, correct coordinate rules, comprehensive strict checks, and pointer/copy tests. Expose the grid inventory and same-object comparisons in the console.

**Phase 3:** Add points 2D/3D and unstructured rank-1 edges/rank-2 mixed mesh to the same object, topology validation, node/edge/face variable examples, primitive-type coverage, and multidimensional caveats. Complete the nine-grid inventory without adding scenarios.

**Phase 4:** Add lifecycle/time examples, tours, generated method matrix, documentation, multiplatform tests and CI.

No phase may waive strict buffer rules to expedite fixtures. If any behavior is unresolved, document the decision and narrow the affected fixture instead of quietly inventing universal BMI semantics.

## 13. Reference index

- CSDMS BMI Python abstract interface: https://github.com/csdms/bmi-python/blob/master/src/bmipy/bmi.py
- CSDMS model grids: https://bmi.csdms.io/en/stable/model_grids.html
- CSDMS BMI grid functions: https://bmi.csdms.io/en/stable/bmi.grid_funcs.html
- CSDMS BMI best practices: https://bmi.csdms.io/en/stable/bmi.best_practices.html
- CSDMS BMI specification: https://github.com/csdms/bmi/blob/develop/docs/source/bmi.spec.md

## 14. Static tactile web companion

Provide `web_demo/index.html`, JavaScript modules, and a stylesheet served by
`python -m http.server` from web_demo. All BMI behavior, mutable state, errors and
visual interactions run in JavaScript; Python is only a static file server. No
backend calls, Python bridge, build step or remote runtime dependency is required.
Vendor D3 with its license for local grid rendering.

The JavaScript class follows the 41-method snake_case surface of
https://github.com/uihilab/BMI-JS/blob/main/bmijs/bmi.js. Its default model mirrors
the nine-grid/21-variable Python baseline. The web companion may provide clearly
labeled selectable geometry variants; switching variants creates a fresh model,
while choosing grids/variables within one variant preserves its identity and time.
These variants do not add standalone scenarios to the Python registry.

Every grid and variable must have a selectable visual representation. Show real
geometry, rank, shape where applicable, variable association, primitive width,
counts/bytes, flat indices and values. Provide node/edge/face selection and typed
indexed writes, grid comparison, explicit method/buffer controls, lifecycle/time,
copy versus live-reference experiments and an accessible call/result/error record.
Rank-3 views are projections with rotation controls; derived structured links
must be identified as display guides rather than invented BMI topology.

Apply the same strict caller-buffer teaching policy to exact TypedArray classes:
no implicit casts, resizing, broadcasting, plain-array acceptance or out-of-range
indices. Validate before any writes; stage overlapping inputs and preserve live
storage identity through setters. Preserve 64-bit integer values with BigInt
arrays/text. Deliberately invalid controls must call the strict implementation
and explain received versus required arguments and the C++ analogy. Distinguish
BMI requirements, grid applicability, C++ parity teaching and Explorer policies.

Do not claim JavaScript models C++ raw-pointer safety or dangling-pointer behavior,
or claim TypedArrays support read-only destinations/strided layouts. Retained
arrays after reset/finalize must be visibly associated with their old owner.
Provide responsive, keyboard-accessible controls, independent JavaScript contract
tests, Python-baseline parity verification, and browser/HTTP smoke checks where
the available environment permits them. Document executed checks and limitations.
