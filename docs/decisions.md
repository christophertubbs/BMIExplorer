# Implementation decisions and remaining scope

The single-scenario migration is implemented. The numbered Phase 1 notes below
retain historical context; decision 7 and the implementation note at the end
describe the current runtime.

1. **Reference contract.** Pin bmipy 2.0.1, subclass its Bmi ABC, and inspect its
   abstract methods programmatically. Tests compare signatures including return
   annotations. Primary sources are the [Python interface](https://github.com/csdms/bmi-python/blob/master/src/bmipy/bmi.py),
   [grid taxonomy](https://bmi.csdms.io/en/stable/model_grids.html) and
   [grid functions](https://bmi.csdms.io/en/stable/bmi.grid_funcs.html).
2. **Applicability.** Uniform geometry uses shape/spacing/origin. Scalar geometry,
   explicit coordinates and topology raise BMIGridOperationError in Phase 1.
   No empty geometry or zero coordinates are fabricated. All methods still exist.
3. **Teaching strictness.** The fixed flat exact-dtype ndarray contract is an
   Explorer policy motivated by C++ typed caller-owned buffers. It is stricter
   than NumPy and some Python BMI models. Native byte order, contiguity, count,
   bounds and destination writeability are checked before writes.
4. **Review policy.** Both exact AI review markers requested by STYLE and SPEC
   are present in authored docstrings pending human review. User guidance files
   remain untouched. Agents.md is used despite its case differing from AGENTS.md.
5. **Configuration.** There are no application environment keys yet. Logging uses
   installed defaults plus an explicit CLI override; domain configuration is a
   built-in scenario token. Avoid an unused environment abstraction until keys exist.
6. **Dependencies.** NumPy and pinned bmipy are direct runtime requirements.
   Upstream bmipy transitive dependencies are retained unchanged. pytest is a
   development extra. The supplied .conda prefix is reused.

7. **Revised scenario scope (2026-11-03).** The requested target is one `all_grids`
   scenario, with all nine grids on one model: scalar rank 0; uniform rectilinear,
   rectilinear, and points at ranks 2 and 3; unstructured at ranks 1 and 2.
   Scalars cannot vary in spatial rank. Two grids per other type make rank
   comparisons possible while retaining representative ranks 0 through 3.
   `vector` and `structured_quadrilateral` are outside required release coverage.
   Shared grids, location comparisons, and time are lessons within the single
   scenario. This supersedes the former separate-scenario/seven-type target;
   the Phase 1 runtime was subsequently migrated as described below.

8. **Single-scenario implementation (2026-11-03).** Model owns immutable ID-to-grid
   and name-to-variable mappings plus independent mutable value arrays. All nine
   grids and ten primitive-width samples coexist. Shared applicability metadata
   drives grid dispatch, reference help, and rank-aware method discovery. Points
   and the edge network return zero counts/exact empty buffers for absent topology;
   inactive coordinate axes raise. The mixed mesh uses an Explorer-authored planar
   topology matching the required 6/8/3 counts and [4,4,3] face sizes. Fixture
   validation checks ranges, face boundaries, winding and variable cardinality.
   Updates evolve primary float64 variables together; static dtype samples avoid
   overflow. Tours and comparisons preserve model identity and state. Old scenario
   selectors fail clearly; only all_grids (or an empty BMI config) initializes.

The requested scenario is implemented. Full release teaching coverage is still
incomplete: all ten tours, detailed method-specific C++ signatures/lessons,
explicit 3D volume-limit demonstrations, and supported-version/platform CI
remain deferred. This does not block comparison of all required grids/ranks on
one live object. The generated matrix covers all five implemented families.
The current matrix and help catalog cover every reference method and the nine
implemented grids; rank-specific coordinate applicability is explicit.

9. **Static web companion (2026-11-03).** User requested a tactile browser UI,
   extending the earlier console-only scope. web_demo implements the linked BMI-JS
   surface independently, with exact TypedArrays as a stricter Explorer teaching
   policy. Baseline metadata mirrors Python; two browser-only geometry variants
   support comparisons without changing the Python registry. D3 is vendored with
   its ISC license; runtime traffic consists only of local static GETs. Live
   references are actual model-owned arrays; copy and old-owner behavior are
   explicit. 64-bit integers use BigInt. No Python model bridge, server API,
   deployment or hosted service is introduced. Tests distinguish real topology
   from derived structured display links and verify location-specific bounds.


10. **Hydrological samples (2026-11-04).** Replaced index-valued `__value` fixtures
    and dtype-named scalar samples with realistic synthetic quantities, matching
    units, and explicit per-hour changes. Existing semantic browser names are
    shared with Python; web metadata is exported from Python descriptors. Slope
    and scalar attributes stay fixed. Defaults remain plausible through end
    time; arbitrary user writes and strict buffer/precision tests still work.
    Exact values, code meanings and scaled-temperature decoding are documented
    in business-configuration.md. These changes supersede earlier index-based
    defaults and the add-one update rule; they do not turn the fixtures into a
    solver or introduce new grids/scenarios.
