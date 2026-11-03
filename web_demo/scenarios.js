/** Deterministic browser-only scenario variants of the Python fixture inventory.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
import { BASELINE } from './fixtures.js';
import { deepFreeze } from './contract.js';

deepFreeze(BASELINE);
export const SCENARIOS = deepFreeze({
  all_grids: { name: 'Explorer baseline', description: 'The same nine grids and 21 variables as BMI Explorer. One object, one shared clock.', scale: [1, 1, 1], offset: [0, 0, 0] },
  stretched_domain: { name: 'Stretched domain', description: 'Double x, halve y, stretch z. Geometry changes; ranks, connectivity and value counts stay the same.', scale: [2, 0.5, 1.5], offset: [0, 0, 0] },
  shifted_domain: { name: 'Shifted domain', description: 'Move x by −120, y by −20 and z by +5. Coordinates can be negative; flat indices still start at zero.', scale: [1, 1, 1], offset: [-120, -20, 5] },
});

/** Create immutable geometry/variable metadata for a selected browser scenario.
 * @param {string} key Registered token. @returns {object} Fresh, frozen descriptor tree.
 * @throws {RangeError} Unknown token; the previous model is never changed.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function scenarioData(key) {
  if (!Object.hasOwn(SCENARIOS, key)) throw new RangeError(`Unknown scenario ${key}. Choose ${Object.keys(SCENARIOS).join(', ')}.`);
  const data = structuredClone(BASELINE);
  const { scale, offset } = SCENARIOS[key];
  for (const grid of data.grids) {
    for (const [index, axis] of ['x', 'y', 'z'].entries()) grid[axis] = grid[axis].map(v => v * scale[index] + offset[index]);
    grid.spacing = grid.spacing.map((v, i) => v * scale[grid.rank - 1 - i]);
    grid.origin = grid.origin.map((v, i) => v * scale[grid.rank - 1 - i] + offset[grid.rank - 1 - i]);
  }
  return deepFreeze(data);
}
