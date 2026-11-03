/** D3 views of geometry and variable locations; coordinates never modify the model.
 * All derived structured links are display guides, not fabricated BMI topology.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */

/** Expand structured coordinates in C order for drawing only.
 * @param {object} grid Immutable grid descriptor. @returns {Array<object>} Nodes with physical x/y/z.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function geometryNodes(grid) {
  if (grid.kind === 'scalar') return [{ index: 0, x: 0, y: 0, z: 0 }];
  if (!grid.shape.length) return grid.x.map((x, index) => ({ index, x, y: grid.y[index] ?? 0, z: grid.z[index] ?? 0 }));
  const [nx, ny = 1, nz = 1] = [...grid.shape].reverse();
  const nodes = [];
  for (let k = 0; k < nz; k += 1) for (let j = 0; j < ny; j += 1) for (let i = 0; i < nx; i += 1) {
    const ij = [i, j, k];
    const xyz = grid.kind === 'uniform_rectilinear'
      ? ['x', 'y', 'z'].map((_, axis) => axis < grid.rank ? grid.origin[grid.rank - 1 - axis] + ij[axis] * grid.spacing[grid.rank - 1 - axis] : 0)
      : [grid.x[i], grid.y[j] ?? 0, grid.z[k] ?? 0];
    nodes.push({ index: (k * ny + j) * nx + i, x: xyz[0], y: xyz[1], z: xyz[2] });
  }
  return nodes;
}

/** Expand exact mesh topology or explicitly derived structured display links.
 * @param {object} grid Geometry descriptor. @returns {{edges:Array,faces:Array}} Drawable index lists.
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function geometryLinks(grid) {
  const edges = [];
  const faces = [];
  for (let i = 0; i < grid.edge_nodes.length; i += 2) edges.push([grid.edge_nodes[i], grid.edge_nodes[i + 1]]);
  let offset = 0;
  for (const count of grid.nodes_per_face) { faces.push(grid.face_nodes.slice(offset, offset + count)); offset += count; }
  if (grid.shape.length) {
    const [nx, ny = 1, nz = 1] = [...grid.shape].reverse();
    for (let k = 0; k < nz; k += 1) for (let j = 0; j < ny; j += 1) for (let i = 0; i < nx; i += 1) {
      const n = (k * ny + j) * nx + i;
      if (i + 1 < nx) edges.push([n, n + 1]);
      if (j + 1 < ny) edges.push([n, n + nx]);
      if (k + 1 < nz) edges.push([n, n + nx * ny]);
    }
  }
  return { edges, faces };
}

/** Render a D3 SVG with clickable nodes/edges/faces and an honest spatial projection.
 * @param {SVGElement} element Destination SVG. @param {object} grid Descriptor.
 * @param {TypedArray} values Selected variable values. @param {object} options View controls.
 * @returns {void} Replaces the SVG children; clicks call options.onSelect(index).
 * TODO(AI-GENERATED): Review and rewrite or approve this implementation.
 * TODO: AI-generated implementation; human review and rewrite required.
 */
export function drawGrid(element, grid, values, options = {}) {
  const d3 = globalThis.d3;
  if (!d3) throw new Error('The bundled D3 library did not load. Check vendor/d3.v7.9.0.min.js.');
  const mini = options.mini ?? false;
  const width = mini ? 220 : 680;
  const height = mini ? 124 : 345;
  const margin = mini ? 18 : 46;
  const location = options.location ?? 'node';
  const nodes = geometryNodes(grid);
  const { edges, faces } = geometryLinks(grid);
  const angle = options.angle ?? -0.5;
  // Rank 3 uses a rotatable orthographic projection; no hidden z axis is fabricated.
  const project = node => grid.rank === 3
    ? [Math.cos(angle) * node.x - Math.sin(angle) * node.z, node.y * .9 + .45 * (Math.sin(angle) * node.x + Math.cos(angle) * node.z)]
    : [node.x, node.y];
  const projected = nodes.map(project);
  const xDomain = d3.extent(projected, p => p[0]);
  const yDomain = d3.extent(projected, p => p[1]);
  const xSpan = xDomain[1] - xDomain[0];
  const ySpan = yDomain[1] - yDomain[0];
  const scale = Math.min((width - 2 * margin) / (xSpan || 1), (height - 2 * margin) / (ySpan || 1));
  const x = value => width / 2 + (value - (xDomain[0] + xDomain[1]) / 2) * scale;
  const y = value => height / 2 - (value - (yDomain[0] + yDomain[1]) / 2) * scale;
  const points = projected.map(p => [x(p[0]), y(p[1])]);
  const numeric = [...values].map(Number);
  const extent = d3.extent(numeric.filter(Number.isFinite));
  const domain = extent[0] === extent[1] ? [extent[0] - 1, extent[1] + 1] : extent;
  const color = d3.scaleSequential(d3.interpolateViridis).domain(domain);
  const svg = d3.select(element).attr('viewBox', `0 0 ${width} ${height}`);
  svg.selectAll('*').remove();
  svg.append('title').text(`${grid.label}: ${grid.kind}, rank ${grid.rank}. ${location} values. Rank 3 uses a rotatable projection.`);
  if (grid.kind === 'scalar') {
    const scalar = svg.append('g').attr('role', mini ? null : 'button').attr('tabindex', mini ? null : 0)
      .attr('aria-label', `Scalar index 0, value ${String(values[0])}`).attr('class', mini ? '' : 'plot-target')
      .on('click', () => options.onSelect?.(0)).on('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); options.onSelect?.(0); }
      });
    const boxWidth = mini ? 100 : 190;
    const boxHeight = mini ? 70 : 120;
    scalar.append('rect').attr('x', (width - boxWidth) / 2).attr('y', (height - boxHeight) / 2)
      .attr('width', boxWidth).attr('height', boxHeight).attr('rx', 8).attr('fill', '#e1e9ce')
      .attr('stroke', mini ? '#a6b98d' : '#c76e3f').attr('stroke-width', mini ? 1 : 2);
    scalar.append('text').attr('x', width / 2).attr('y', height / 2 + 5).attr('text-anchor', 'middle')
      .attr('fill', '#244b43').attr('font-family', 'Georgia, serif').attr('font-size', mini ? 25 : 35)
      .text(String(values[0]));
    scalar.append('text').attr('x', width / 2).attr('y', height / 2 + (mini ? 23 : 32)).attr('text-anchor', 'middle')
      .attr('class', 'axis-caption').text('one value · rank 0');
    if (!mini) svg.append('text').attr('x', width / 2).attr('y', height - 23).attr('text-anchor', 'middle')
      .attr('class', 'axis-caption').text('No spatial axes · storage still occupies memory');
    return;
  }
  const group = svg.append('g');
  const tooltip = (kind, index) => {
    const value = location === kind ? ` · value ${String(values[index])}` : '';
    const coords = kind === 'node' ? ` · (${['x', 'y', 'z'].slice(0, grid.rank).map(axis => nodes[index][axis]).join(', ')})` : '';
    return `${kind} ${index}${value}${coords}`;
  };
  const bind = (selection, kind) => {
    selection.append('title').text((_, i) => tooltip(kind, i));
    if (!mini && location === kind) {
      selection.attr('tabindex', 0).attr('role', 'button').attr('aria-label', (_, i) => `Select ${tooltip(kind, i)}`)
        .on('click', function(event, datum) { options.onSelect?.(Number(this.dataset.index)); })
        .on('keydown', function(event) { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); options.onSelect?.(Number(this.dataset.index)); } });
    }
  };
  const faceSelection = group.selectAll('polygon').data(faces).join('polygon')
    .attr('points', face => face.map(n => points[n].join(',')).join(' '))
    .attr('data-index', (_, i) => i)
    .attr('fill', (_, i) => location === 'face' ? color(numeric[i]) : '#dedfcd')
    .attr('fill-opacity', location === 'face' ? .85 : .5)
    .attr('stroke', (_, i) => location === 'face' && i === options.selected ? '#e36539' : '#b7bda9')
    .attr('stroke-width', (_, i) => location === 'face' && i === options.selected ? 4 : 1.5)
    .attr('class', location === 'face' ? 'plot-target' : '');
  bind(faceSelection, 'face');
  const edgeSelection = group.selectAll('line').data(edges).join('line')
    .attr('x1', edge => points[edge[0]][0]).attr('y1', edge => points[edge[0]][1])
    .attr('x2', edge => points[edge[1]][0]).attr('y2', edge => points[edge[1]][1])
    .attr('data-index', (_, i) => i)
    .attr('stroke', (_, i) => location === 'edge' ? i === options.selected ? '#e36539' : color(numeric[i]) : '#b6c3bc')
    .attr('stroke-width', location === 'edge' ? 9 : mini ? 1.5 : 2)
    .attr('class', location === 'edge' ? 'plot-target' : '')
    .attr('stroke-linecap', 'round');
  bind(edgeSelection, 'edge');
  const nodeSelection = group.selectAll('circle').data(nodes).join('circle')
    .attr('cx', (_, i) => points[i][0]).attr('cy', (_, i) => points[i][1])
    .attr('data-index', node => node.index)
    .attr('r', mini ? 3.8 : location === 'node' ? 12 : 5)
    .attr('fill', node => location === 'node' ? color(numeric[node.index]) : '#244b43')
    .attr('stroke', node => location === 'node' && node.index === options.selected ? '#e36539' : '#faf9f3')
    .attr('stroke-width', node => location === 'node' && node.index === options.selected ? 4 : 2)
    .attr('class', location === 'node' ? 'plot-target' : '');
  bind(nodeSelection, 'node');
  if (!mini && options.labels !== false) {
    group.selectAll('text.node-label').data(nodes).join('text').attr('class', 'node-label')
      .attr('x', (_, i) => points[i][0]).attr('y', (_, i) => points[i][1] - 19)
      .attr('text-anchor', 'middle').text(node => node.index);
  }
  if (!mini) {
    svg.append('text').attr('x', 15).attr('y', height - 14).attr('class', 'axis-caption')
      .text(grid.kind === 'scalar' ? 'No spatial axes · one logical value' : grid.rank === 3 ? '3D orthographic projection · turn the view to see z' : `x →  ·  ${grid.rank >= 2 ? 'y ↑' : 'x-axis network'}`);
    if (grid.shape.length) svg.append('text').attr('x', width - 16).attr('y', height - 14).attr('text-anchor', 'end').attr('class', 'axis-caption').text('Lines = derived display guides');
  }
}
