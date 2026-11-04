/** Optional real-browser behavioral checks; Playwright is test tooling only.
 * Usage: NODE_PATH=<temporary-tools>/node_modules node browser-smoke.cjs <base-url>
 * Screenshots go only under TMPDIR, which must be set. No model backend is used.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

/** Run actual clicks, typed edits, model transitions and responsive checks.
 * @returns {Promise<void>} Resolves after all assertions/screenshots and browser cleanup.
 * @throws {Error} UI, browser, network isolation or contract behavior failed.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
async function main() {
  assert.ok(process.env.TMPDIR, 'Set TMPDIR for browser artifacts.');
  const artifacts = path.join(process.env.TMPDIR, 'bmi-explorer-web-checks');
  fs.mkdirSync(artifacts, { recursive: true });
  const base = process.argv[2] || 'http://127.0.0.1:8000';
  const origin = new URL(base).origin;
  const browser = await chromium.launch({ headless: true });
  const errors = [];
  const requests = [];
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
    page.on('pageerror', error => errors.push(error.message));
    page.on('request', request => requests.push([request.method(), request.url()]));
    page.on('response', response => { if (response.status() >= 400) errors.push(`HTTP ${response.status()} ${response.url()}`); });
    await page.goto(base);
    await page.waitForSelector('#main-grid circle');
    await page.locator('[data-variable="uniform_2d__slope"]').click();
    assert.equal(await page.locator('.fatal-message').count(), 0);
    assert.equal(await page.locator('[data-variable]').count(), 21);
    assert.equal(await page.locator('#method option').count(), 41);
    assert.equal(await page.locator('#main-grid circle').count(), 12);
    await page.screenshot({ path: path.join(artifacts, 'desktop.png'), fullPage: true });

    await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /Int32Array\(2\) \[3, 4\]/);
    assert.match(await page.locator('#latest-result').innerText(), /destination: true/);
    await page.locator('#method').selectOption('get_grid_spacing');
    await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /Float64Array\(2\) \[2, 5\]/);
    await page.locator('[data-variable="rectilinear_2d__precip_rate"]').click();
    await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /BMIGridOperationError/);
    assert.match(await page.locator('#latest-result').innerText(), /Caller buffer after rejection/);
    await page.locator('#method').selectOption('get_grid_x');
    assert.equal(await page.locator('#buffer-length').inputValue(), '4');
    await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /\[100, 102, 107, 115\]/);
    await page.locator('[data-variable="points_2d__snow_depth"]').click();
    assert.equal(await page.locator('#buffer-length').inputValue(), '6');
    assert.equal(await page.locator('#main-grid circle').count(), 6);
    assert.equal(await page.locator('#main-grid line').count(), 0);
    await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /\[0, 2, 3, 1, -1, 1\]/);

    await page.locator('[data-variable="rectilinear_2d__precip_rate"]').click();
    await page.locator('#capture-memory').click();
    await page.locator('#copy-edit').click();
    assert.equal(await page.locator('#copy-values .memory-cell').first().innerText(), '11.2');
    assert.equal(await page.locator('#pointer-values .memory-cell').first().innerText(), '1.2');
    await page.locator('#pointer-edit').click();
    assert.equal(await page.locator('[data-value-index="0"] strong').innerText(), '11.2');
    await page.locator('#step').click();
    assert.equal(await page.locator('#model-time').innerText(), '3,600 s');
    assert.equal(await page.locator('#pointer-values .memory-cell').first().innerText(), '11.45');
    assert.equal(await page.locator('#copy-values .memory-cell').first().innerText(), '11.2');

    await page.locator('#method').selectOption('set_value');
    await page.locator('#source-values').fill(Array.from({ length: 12 }, (_, i) => i + 20).join(', '));
    await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /ACCEPTED/);
    assert.equal(await page.locator('#pointer-values .memory-cell').first().innerText(), '20');
    assert.equal(await page.locator('#copy-values .memory-cell').first().innerText(), '11.2');
    await page.locator('#main-grid circle[data-index="6"]').click();
    assert.equal(await page.locator('#selected-index').inputValue(), '6');
    await page.locator('#edit-value').fill('77');
    await page.locator('#write-value').click();
    assert.equal(await page.locator('[data-value-index="6"] strong').innerText(), '77');
    assert.equal(await page.locator('#pointer-values .memory-cell').nth(6).innerText(), '77');
    await page.locator('#compare-grid').selectOption('3'); await page.locator('#compare').click();
    assert.match(await page.locator('#comparison').innerText(), /Same BMI object/);
    assert.equal(await page.locator('#model-time').innerText(), '3,600 s');

    await page.locator('.mistake-menu summary').click();
    for (const [mistake, category] of [['array', 'BMITypeError'], ['dtype', 'BMITypeError'], ['length', 'BMIBufferError'], ['broadcast', 'BMITypeError']]) {
      await page.locator(`[data-mistake="${mistake}"]`).click();
      assert.match(await page.locator('#latest-result').innerText(), new RegExp(category));
      assert.equal(await page.locator('[data-value-index="6"] strong').innerText(), '77');
    }

    await page.locator('[data-variable="unstructured_mixed__precipitation_rate"]').click();
    assert.equal(await page.locator('#main-grid polygon').count(), 3);
    assert.equal(await page.locator('.value-chip').count(), 3);
    await page.locator('#main-grid polygon[data-index="2"]').click();
    assert.equal(await page.locator('#selected-index').inputValue(), '2');
    await page.locator('#edit-value').fill('55'); await page.locator('#write-value').click();
    assert.equal(await page.locator('[data-value-index="2"] strong').innerText(), '55');
    await page.locator('[data-mistake="bounds"]').click();
    assert.match(await page.locator('#latest-result').innerText(), /BMIIndexError/);
    await page.locator('[data-variable="unstructured_mixed__flux"]').click();
    assert.equal(await page.locator('.value-chip').count(), 8);
    await page.locator('#main-grid line[data-index="7"]').click();
    assert.equal(await page.locator('#selected-index').inputValue(), '7');

    await page.locator('[data-variable="scalar__processed_cells"]').click();
    await page.locator('#edit-value').fill('18446744073709551615');
    await page.locator('#write-value').click();
    assert.equal(await page.locator('[data-value-index="0"] strong').innerText(), '18446744073709551615n');
    await page.locator('#edit-value').fill('18446744073709551616'); await page.locator('#write-value').click();
    assert.match(await page.locator('#latest-result').innerText(), /BMITypeError/);
    assert.equal(await page.locator('[data-value-index="0"] strong').innerText(), '18446744073709551615n');

    await page.locator('[data-variable="points_3d__water_level"]').click();
    assert.equal(await page.locator('#rotation-control').isVisible(), true);
    const beforeTurn = await page.locator('#main-grid circle').evaluateAll(nodes => nodes.map(n => n.getAttribute('cx')));
    await page.locator('#rotation').evaluate(element => { element.value = '85'; element.dispatchEvent(new Event('input', { bubbles: true })); });
    const afterTurn = await page.locator('#main-grid circle').evaluateAll(nodes => nodes.map(n => n.getAttribute('cx')));
    assert.notDeepEqual(afterTurn, beforeTurn);
    await page.locator('#main-grid circle[data-index="3"]').focus();
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('#selected-index').inputValue(), '3');

    await page.locator('#atlas-tab').click();
    assert.equal(await page.locator('.atlas-card svg').count(), 9);
    assert.equal(await page.locator('[data-atlas-variable]').count(), 21);
    await page.screenshot({ path: path.join(artifacts, 'atlas.png'), fullPage: true });
    await page.locator('[data-atlas-variable="uniform_2d__slope"]').click();
    await page.locator('#finalize').click();
    assert.equal(await page.locator('#model-status').innerText(), 'FINALIZED');
    await page.locator('#method').selectOption('get_component_name'); await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /BMILifecycleError/);
    assert.equal(await page.locator('#pointer-status').innerText(), 'RETAINED OLD OWNER');
    await page.locator('#reset').click();
    assert.equal(await page.locator('#model-time').innerText(), '0 s');
    assert.equal(await page.locator('[data-value-index="6"] strong').innerText(), '0.0113');
    await page.locator('#pointer-edit').click();
    assert.equal(await page.locator('[data-value-index="0"] strong').innerText(), '0.0124');
    assert.match(await page.locator('#latest-result').innerText(), /current model is unchanged/i);

    await page.locator('#scenario').selectOption('shifted_domain');
    await page.locator('[data-variable="rectilinear_2d__precip_rate"]').click();
    await page.locator('#method').selectOption('get_grid_x'); await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /\[-20, -18, -13, -5\]/);
    await page.locator('#scenario').selectOption('stretched_domain');
    await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /\[200, 204, 214, 230\]/);
    await page.locator('#scenario').selectOption('all_grids');
    await page.locator('#open-guide').click(); assert.equal(await page.locator('#guide').isVisible(), true);
    await page.keyboard.press('Escape'); assert.equal(await page.locator('#guide').isVisible(), false);

    await page.setViewportSize({ width: 390, height: 844 });
    await page.locator('[data-variable="uniform_2d__slope"]').click();
    await page.locator('#method').selectOption('get_grid_shape');
    await page.locator('#run-call').click();
    assert.match(await page.locator('#latest-result').innerText(), /Int32Array\(2\) \[3, 4\]/);
    const overflow = await page.evaluate(() => ({ width: innerWidth, scroll: document.documentElement.scrollWidth }));
    assert.ok(overflow.scroll <= overflow.width, `Mobile page overflows: ${JSON.stringify(overflow)}`);
    await page.screenshot({ path: path.join(artifacts, 'mobile.png'), fullPage: true });
    assert.deepEqual(errors, []);
    assert.ok(requests.every(([method, url]) => method === 'GET' && new URL(url).origin === origin), 'Unexpected backend or external network request.');
    console.log('Browser checks passed: 41 controls, 9 D3 grids, 21 variables, typed reads/writes/errors, copy/reference ownership, topology locations, BigInt, 3D rotation, keyboard, lifecycle/reset, variants, mobile layout and local GET-only traffic.');
    console.log('Screenshots:', artifacts);
  } finally { await browser.close(); }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
