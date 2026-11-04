# Fixture configuration

The sole domain input is the built-in token `all_grids`, supplied to
`Model.initialize(config_file)` or `--scenario all_grids`. An empty BMI config
string also selects this default. No configuration file is read. Other names
fail explicitly. The console initializes all grids before opening Python input.
The immutable registry is `bmi_explorer.fixtures.SCENARIOS`; descriptors contain
tuples, while each model allocates its own mutable NumPy value buffers.

| ID | Label | Type | Rank | Nodes | Geometry |
|---|---|---|---:|---:|---|
| 0 | scalar | scalar | 0 | 1 | No spatial axes |
| 1 | uniform_2d | uniform_rectilinear | 2 | 12 | shape [3,4], spacing [2,5], origin [10,100] |
| 2 | uniform_3d | uniform_rectilinear | 3 | 24 | shape [2,3,4], spacing [7,2,5], origin [0,10,100] |
| 3 | rectilinear_2d | rectilinear | 2 | 12 | shape [3,4], explicit x/y axes |
| 4 | rectilinear_3d | rectilinear | 3 | 24 | shape [2,3,4], explicit x/y/z axes |
| 5 | points_2d | points | 2 | 6 | Per-node x/y, no edges/faces |
| 6 | points_3d | points | 3 | 6 | Per-node x/y/z, no edges/faces |
| 7 | unstructured_edges | unstructured | 1 | 4 | x=[0,2,5,9], edges 0→1→2→3, no faces |
| 8 | unstructured_mixed | unstructured | 2 | 6 | Two quadrilaterals and a triangle; eight edges |

IDs are stable in this scenario, but examples should derive them with
`get_var_grid(name)`. Variable names describe synthetic hydrological quantities;
they are illustrative, not certified Standard Names or observed data. All primary
node/edge/face quantities use float64. Their exact arrays live in
`src/bmi_explorer/fixtures.py`; the browser baseline is exported from those same
descriptors. Browser geometry variants keep these values and units.

| Variable | Units | Initial values or range | Change per hour |
|---|---|---|---:|
| scalar__velocity | m s-1 | 1.25 | +0.05 |
| uniform_2d__slope | 1 (rise/run) | 0.0036–0.0189 | 0 |
| uniform_3d__soil_temp | degC | 12.2–14.8; cooler second layer | +0.1 |
| rectilinear_2d__precip_rate | mm h-1 | 1.2–4.0 | +0.25 |
| rectilinear_3d__saturation | 1 (fraction) | 0.45–0.85; wetter second layer | +0.01 |
| points_2d__snow_depth | m | 0.10–0.32 | -0.002 |
| points_3d__water_level | m above local datum | 0.846–4.42 | +0.02 |
| unstructured_edges__flow_velocity | m s-1 | 1.773–2.435 | +0.05 |
| unstructured_mixed__depth | m | 1.238–4.976 | +0.01 |
| unstructured_mixed__flux | m3 s-1 | -0.119–1.351 | +0.02 |
| unstructured_mixed__precipitation_rate | mm h-1 | [2.0, 2.5, 3.0] | +0.25 |

The mixed mesh has six depth values on nodes, eight signed volumetric fluxes
on edges, and three rainfall rates on faces. Negative flux denotes flow against
the edge's tail-to-head direction. Water levels use an arbitrary local vertical
datum, independent of the small illustrative grid coordinates. All units above
are returned by `get_var_units` (`m` for water level).

Ten static scalar attributes preserve primitive-width teaching coverage:

| Variable | Dtype | Initial value | Units/meaning |
|---|---|---:|---|
| scalar__anomaly_class | int8 | -3 | 1; illustrative class -3 (very dry) to +3 (very wet) |
| scalar__qc_code | uint8 | 2 | 1; example quality flag: 0 unchecked, 1 good, 2 suspect, 3 rejected |
| scalar__scaled_temp | int16 | 2345 | 0.01 degC; decoded air temperature is 23.45 °C |
| scalar__stream_order | uint16 | 5 | 1; Strahler stream order |
| scalar__flow_direction_code | int32 | 64 | 1; D8 bit code, north in this fixture |
| scalar__contributing_cells | uint32 | 384 | 1; upstream grid-cell count |
| scalar__storage_capacity | int64 | 7030259239 | m3; large reservoir capacity |
| scalar__processed_cells | uint64 | 83939242345 | 1; cumulative cell visits across timesteps/runs |
| scalar__area_sqkm | float32 | 253.25 | km2; catchment area |
| scalar__manning_roughness | float64 | 0.035 | s m-1/3; Manning n |

Counts and codes are dimensionless. The scaled temperature explicitly uses
hundredths of a degree; its integer value is not a temperature of 2345 °C.
These independent examples do not describe one calibrated catchment. See
[type mapping](type-mapping.md) for buffer widths and ABI assumptions.

Shape/spacing/origin use ij order, with x varying fastest in flat C-order node
storage. On shape [3,4], row 1, column 2 is index 6. On shape [2,3,4], layer 1,
row 1, column 2 is index 18. Uniform 2D starts at (x=100,y=10) and ends at
(x=115,y=14). Uniform 3D adds layers z=0 and z=7. Rectilinear axes are
x=[100,102,107,115], y=[10,11,14], and (3D only) z=[0,7]. Their x/y coordinate
buffers have lengths 4/3, rather than one entry per node. Rectilinear spacing and
origin calls fail; users can compute such quantities outside BMI.

Point grids and the mixed mesh share node coordinates
x=[0,2,3,1,-1,1], y=[0,0,2,3,2,1]. Points 3D adds z=[0,1,4,2,5,3]. All point
coordinate buffers have six entries; point grid rank means active spatial axes,
not the number of points or the rank of its flat value buffer. Points have zero
edges/faces. Their topology count getters and exact empty int32 topology buffers
succeed by Explorer policy. The rank-1 edge mesh similarly accepts empty face
buffers. Scalar has no geometry/topology calls. Uniform explicit coordinates and
all implicit structured topology calls fail. Missing axes fail (e.g. z on rank 2),
rather than returning synthetic zero coordinates. These applicability choices
follow the [BMI grid taxonomy](https://bmi.csdms.io/en/stable/model_grids.html)
with explicit Explorer policies for zero topology and scalar storage.

The mixed mesh is an Explorer-authored planar example. Its five boundary nodes
0–4 surround interior node 5. Edges (tail/head pairs) are
`[(0,1),(1,2),(2,3),(3,4),(4,0),(1,5),(3,5),(0,5)]`.
Counter-clockwise face boundaries are `[[1,2,3,5],[3,4,0,5],[0,1,5]]`, with matching
edge IDs `[[1,2,6,5],[3,4,7,6],[0,5,7]]`. Thus nodes_per_face=[4,4,3], flat
edge_nodes length=16, flat face_nodes/face_edges lengths=11. Slice using cumulative
face sizes; reshaping all faces into four-node rows is invalid. Initialization
validates node/edge ranges, boundary consistency, winding, and variable counts.
The same coordinates on a point grid illustrate how explicit connectivity changes
available operations without changing node positions.

Every grid shares one clock: start/current=0 seconds, step=3600, end=10800.
Each step applies the per-hour `step_change` in the table above to evolving
variables; slope and scalar attributes remain fixed. Snow slowly melts, temperatures
warm slightly, and saturation stays between zero and one through the final step.
These deterministic changes demonstrate shared time and live buffers, not coupled
physics. User writes remain unrestricted by physical range, so memory/precision
experiments keep their existing behavior. Reset restores the plausible defaults. `update_until` requires a finite exact step
boundary between current and end inclusive. Writes affect only their named
variable; comparisons, discovery and tours do not update, reset or replace state.

Value buffers are exact native flat C-contiguous ndarrays. Sources may be
read-only; destinations must be writable. Indices are int32. Duplicate indexed
writes use the last source entry; empty indexed calls are valid. Inputs are
staged to preserve deterministic writes when buffers overlap. Scalar uses one
logical node and a one-element buffer by Explorer convention.

Initialize is allowed once per new model. Finalize invalidates every BMI call.
`explorer.reset()` or compatibility `explorer.use('all_grids')` replaces the whole
model and restores all initial values, grid IDs and time. Retained Python arrays
can survive but are detached from the new model; C++ raw pointers may instead
become invalid after their owner's lifetime ends. No lifetime-safety equivalence
is claimed. Rank-3 geometry does not supply arbitrary 3D volume connectivity.
