# BMI Explorer

Explore CSDMS Basic Model Interface calls in an ordinary Python console with
real, stateful NumPy storage and strict caller-allocated buffer checks.

The single `all_grids` scenario exposes **nine grids on one BMI object**:

| Grid labels | BMI type | Ranks |
|---|---|---|
| scalar | scalar | 0 |
| uniform_2d, uniform_3d | uniform_rectilinear | 2, 3 |
| rectilinear_2d, rectilinear_3d | rectilinear | 2, 3 |
| points_2d, points_3d | points | 2, 3 |
| unstructured_edges, unstructured_mixed | unstructured | 1, 2 |

The model subclasses the pinned `bmipy.Bmi` interface and implements every
reference method. Methods unavailable for a grid's family or rank raise an
explanatory exception before changing any destination buffer.

Use the existing project environment:

```sh
.conda/bin/python -m bmi_explorer
.conda/bin/bmi-explorer --list
```

After installation in an activated environment, both `python -m bmi_explorer`
and `bmi-explorer` work from any directory. See [installation](docs/installation.md)
for conda and uv setup.

A [tactile web companion](web_demo/README.md) runs the model entirely in JavaScript
with D3 grid views, selectable demonstration models, typed-buffer experiments and
copy/reference controls. Serve its static files locally:

```sh
cd web_demo
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000`. Python serves files only; no model calls go to Python.

All of these queries use the same initialized model:

```python
>>> u = bmi.get_var_grid('uniform_2d__value')
>>> r = bmi.get_var_grid('rectilinear_2d__value')
>>> p = bmi.get_var_grid('points_2d__value')
>>> bmi.get_grid_shape(u, np.empty(2, dtype=np.int32))
array([3, 4], dtype=int32)
>>> bmi.get_grid_spacing(u, np.empty(2, dtype=np.float64))
array([2., 5.])
>>> bmi.get_grid_x(r, np.empty(4, dtype=np.float64))
array([100., 102., 107., 115.])
>>> bmi.get_grid_x(p, np.empty(6, dtype=np.float64))
array([ 0.,  2.,  3.,  1., -1.,  1.])
>>> explorer.try_call('get_grid_spacing', r, np.empty(2, dtype=np.float64))
# BMIGridOperationError: rectilinear axes do not have uniform spacing.
>>> print(explorer.compare(u, r))
>>> print(explorer.topology(bmi.get_var_grid('unstructured_mixed__value')))
```

Use `explorer.list()` for IDs, labels, types, ranks, geometry lengths, and variable
names/counts/bytes/dtypes. BMI has no grid-enumeration method; IDs can also be
collected from `get_var_grid(name)` over input/output variable names.
Each grid has a float64 node variable `<grid_label>__value`. The mixed mesh also
has edge and face variables; ten typed scalar samples demonstrate primitive widths.

`np`, initialized `bmi`, `explorer`, read-only `scenarios` (only `all_grids`), and
`help_bmi` are preloaded. Try `help_bmi('get_value')`, `explorer.describe(u)`,
`explorer.methods(u)`, or `explorer.example('get_grid_x', grid_id=r)`.
Normal multiline Python and `help()` work; errors leave the console usable.
Readline history/editing is available when the runtime provides it.

`explorer.reset()` restores all grids, values, IDs, and time together on a fresh
model. Previously retained arrays remain detached from the replacement. Grid
comparisons and tours preserve the current object and values.

Options: `--scenario all_grids` (the default), `--list`, `--tour scalar`,
`--tour buffers`, `--tour grids`, `--no-banner`, `--strict`, and
`--log-override PATH`. Strict validation is always on. Former standalone scenario
tokens such as `scalar` and `uniform_2d` are rejected. `explorer.use('all_grids')`
is a compatibility reset, not a way to select individual grids. The console runs
local Python with the user's normal privileges; `exit()` or EOF exits.

Read [fixture policies](docs/business-configuration.md),
[type mapping](docs/type-mapping.md), [method matrix](docs/grid-matrix.md),
[decisions and remaining scope](docs/decisions.md), and the
[console smoke example](docs/console-smoke.md). Advanced lessons and multiplatform
CI from SPEC remain future work.

Development checks:

```sh
.conda/bin/python -m pytest -q
```
