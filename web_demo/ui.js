/** Small DOM and primitive-formatting helpers shared by the static workbench.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */

/** Resolve a required UI element; fail visibly on an incomplete document.
 * @param {string} id HTML ID. @returns {HTMLElement} Existing element.
 * @throws {Error} Missing markup.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function byId(id) {
  const element = document.getElementById(id);
  if (!element) throw new Error(`Missing interface element #${id}.`);
  return element;
}

/** Create safe text-only DOM; user values never become HTML.
 * @param {string} tag Element name. @param {string} text Text content.
 * @param {string} className Optional CSS class. @returns {HTMLElement} New node.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function node(tag, text = '', className = '') {
  const element = document.createElement(tag);
  element.textContent = text;
  element.className = className;
  return element;
}

/** Append a labeled option without HTML interpolation.
 * @param {HTMLElement} parent Select or optgroup. @param {string|number} value Value.
 * @param {string} text Visible label. @returns {void}
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function option(parent, value, text) {
  const element = node('option', text);
  element.value = String(value);
  parent.append(element);
}

/** Format values without losing integer width or BigInt precision.
 * @param {unknown} value Returned primitive or typed memory. @returns {string} Readable contract result.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function format(value) {
  if (value === undefined) return 'undefined (operation completed)';
  if (typeof value === 'bigint') return value.toString() + 'n';
  if (typeof value === 'number') return Object.is(value, -0) ? '−0' : String(value);
  if (ArrayBuffer.isView(value)) return `${value.constructor.name}(${value.length}) [${[...value].map(format).join(', ')}]`;
  if (Array.isArray(value)) return `[${value.map(format).join(', ')}]`;
  return String(value);
}

/** Serialize primitive values as explicit caller input (BigInt stays integer text).
 * @param {Iterable<number|bigint>} values Numeric values. @returns {string} Comma-separated text.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function inputText(values) { return [...values].map(value => Object.is(value, -0) ? '-0' : String(value)).join(', '); }
