# The model lab

A static, tactile companion to BMI Explorer. All model state and BMI calls run
in JavaScript. Python serves files only; there is no API, Python bridge, database,
build step, package installation, CDN request or internet requirement to use it.

From the project root, using an activated Python environment:

```sh
cd web_demo
python -m http.server 8000 --bind 127.0.0.1
```

Open [the local demo](http://localhost:8000). With the supplied project environment,
`../.conda/bin/python -m http.server 8000 --bind 127.0.0.1` also works from web_demo.
Use HTTP rather than opening index.html directly: the browser loads ES modules.

## Play with the interface

- Select a variable in the inventory; its grid, values, dtype, bytes and
  node/edge/face location appear together. Selection preserves the model and clock.
- Open **Grid atlas** for D3 representations of all nine grids, with a selectable
  representation of every variable. Open a grid or variable to inspect its state.
- Click a plotted node, edge or face (or its flat value chip) and use the indexed
  write control. Typed source construction is explicit; index ranges follow the
  variable's location, not necessarily the grid's node count.
- Choose any of the 41 BMI methods in **Make a BMI call**. For array methods,
  explicitly choose caller memory type and element count. Getters show whether
  they returned the identical destination. Source text constructs typed caller
  memory; setters never cast, resize, pad or broadcast that memory.
- Use a deliberate-mistake button to test plain arrays, wrong widths, wrong counts,
  out-of-range indices, unsupported geometry or scalar broadcasting. Read the
  expected/received contract and retained destination sentinel in the record.
- Capture a **copy + live reference**, edit either, then step the model. The copy
  stays independent; the reference follows its model's storage. Reset/switch models
  and inspect the visibly detached old-owner reference.
- Compare grids without switching models. Rectilinear coordinates have lengths
  per axis; point coordinates have lengths per node. Rank-3 views have a rotation
  slider, with real z coordinates in each node's tooltip.
- Finalize the model, then try another BMI call. Finalization is a lifecycle
  boundary. Reset creates a new owner rather than resurrecting the old object.

## Models, geometry and policies

The default **Explorer baseline** mirrors the Python all_grids fixture exactly:
scalar rank 0; uniform/rectilinear/points ranks 2 and 3; unstructured ranks 1 and 2.
All nine grids and 21 variables coexist on one model. Ten static scalar samples
cover int8/uint8 through int64/uint64 and float32/float64. Mixed-mesh node, edge and
face variables have 6/8/3 values. Baseline coordinates, shape/order and connectivity
are documented in [fixture configuration](../docs/business-configuration.md).

The companion adds two explicitly browser-local model variants:

| Model | Geometry transformation | What stays the same |
|---|---|---|
| Explorer baseline | None | Python fixture metadata |
| Stretched domain | x × 2, y × 0.5, z × 1.5 | Rank, topology, cardinalities, initial values |
| Shifted domain | x − 120, y − 20, z + 5 | Rank, topology, cardinalities, initial values |

Switching models/reset replaces the whole owner and resets time to 0. Grid and
variable selection never do so. Every model uses a shared 3600 s step and a
10800 s end; evolving hydrological values change by their documented quantity-specific
hourly increment each step, while primitive-width samples stay static. There are no timed simulations.

The public method names and argument order follow the linked
[BMI-JS skeleton](https://github.com/uihilab/BMI-JS/blob/main/bmijs/bmi.js).
This is an independent implementation of that surface. See the official
[BMI grid taxonomy](https://bmi.csdms.io/en/stable/model_grids.html) and
[grid methods](https://bmi.csdms.io/en/stable/bmi.grid_funcs.html).
The interface's original Array descriptions are intentionally tightened here:

- **BMI required:** variable/grid identities, method surface, metadata, caller
  destinations, copy/reference behavior and model lifecycle.
- **Grid-type applicability:** coordinate arrays versus shape/spacing/origin,
  active axes, explicit connectivity and informative unsupported-method errors.
- **C++ parity teaching:** exact primitive type and count, flat index buffers,
  validation before writes, no silent casting/broadcasting, staged overlapping
  inputs and pointer-preserving setters.
- **Explorer policy:** exact native fixed-buffer TypedArray classes; Int32Array
  indices/topology; Float64Array coordinates; scalar one-element storage; empty
  point/edge-network face topology; timestep and initialization rules. These are
  not universal restrictions imposed on every BMI model or language binding.

TypedArrays use contiguous native memory. Fixed contiguous subviews are accepted;
subclasses, DataView, shared/resizable/detached buffers and ordinary arrays are
rejected. JavaScript cannot express strided TypedArrays or enforce a read-only
TypedArray destination. Buffer lifetime and writeability are therefore not a
simulation of C++ pointer safety. Prior references can survive finalization;
raw C++ pointers have no corresponding guarantee.

Int64/uint64 use BigInt64Array/BigUint64Array and integer text, preserving all
64 bits. UI parsing checks range/fractions before constructing memory, avoiding
TypedArray constructors' permissive integer wrapping. Float32 construction is
an explicit caller conversion; model methods accept only the declared dtype.
The plot uses a Number conversion for color/position only; exact BigInt values
remain in labels, value chips, controls and trace. 3D plots are orthographic
projections. Structured plot links are derived guides, not extra supported BMI
connectivity. No general volume/cell topology interface is invented.

## Files and development checks

`index.html`/`styles.css` define the responsive interface. `app.js` composes controls
and read-only views. `bmi.js` implements the 41 methods; `contract.js` centralizes
buffers/applicability; `operations.js` drives method help; `scenarios.js` constructs
immutable variants; `fixtures.js` is the checked-in baseline; `visualization.js`
derives D3 display geometry; `ui.js` contains text-only DOM helpers.

D3 7.9.0 is bundled under vendor with its original ISC license. No third-party
JavaScript executes from a remote service. Modern browsers with ES modules,
private fields, structuredClone, dialog and BigInt TypedArrays are required.
Node is needed only to run development tests, not to serve/use the page.

```sh
cd web_demo
npm test
```

The tests use Node's built-in test runner and no installed test packages (validated
with Node 25.8.2). From the project root, the Python fixture parity test verifies
that the baseline's every descriptor/coordinate/connectivity entry still matches
Python. The model never imports or communicates with Python during use.

Optional real-browser smoke checks are in `tests/browser-smoke.cjs`. They require
Playwright/Chromium as separate development tooling; neither is a demo dependency.
Serve the demo, set TMPDIR for screenshots, then run:

```sh
NODE_PATH="$TMPDIR/bmi-explorer-web-tools/node_modules" \
  node tests/browser-smoke.cjs http://127.0.0.1:8000
```

Use the installed Playwright browser location (PLAYWRIGHT_BROWSERS_PATH if it is
not the default). Host-specific library setup belongs to the test environment,
not this project. Browser checks cover actual controls, D3 element counts,
copy/reference mutations and owner replacement, errors preserving values,
node/edge/face selection, full 64-bit text, 3D rotation, keyboard interaction,
scenario variants, mobile overflow, and exclusively same-origin GET traffic.


The baseline and both geometry variants use the same synthetic hydrological data
as Python: soil temperature in degC, rainfall in mm h-1, fractional saturation,
depths in m, velocity in m s-1, and edge discharge in m3 s-1. Slope and scalar
attributes stay fixed. See [fixture values and units](../docs/business-configuration.md)
for exact meanings, ranges and per-hour changes. Integer scaled temperature 2345
means 23.45 °C; it is stored in 0.01 degC units. These samples demonstrate BMI
storage and shared time, not hydrological physics.
