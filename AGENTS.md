# Bihar Assembly Map — Choropleth Plan and Conventions

This document captures the design and implementation plan for the SVG/D3 choropleth (and a Leaflet variant where relevant). Refer to this when continuing work.

## Context

- Primary viewer: `index_svg.html` (SVG + D3 v7).
- Data sources:
  - Boundaries: `bihar_ac_all.geojson` (FeatureCollection of AC polygons).
  - Attributes: `bihar_election_results_consolidated.csv` (joined by zero‑padded `AC_NO` ↔ `no`).
- Local helpers created earlier: `bihar_ac_geojson/` (per‑AC files for other flows).

## Shared State and Configuration

- `state`: `{ metricId, classification, breaks, zoomTransform, selectedKey }`.
- `metrics` (examples):
  - `alliance`: categorical, palette `{ NDA, MGB, UPA, OTH, IND }`.
  - `margin20|margin15|margin10`: numeric; derive from CSV cols `y2020_margin`, etc.
- `scales` factory (based on `classification`): `threshold | quantile | quantize | sequential`.
- Number formatting: Indian locale (1,23,456) for legend/tooltip.

## Modules To Implement (SVG/D3)

1) Zoom (d3-zoom)
- Attach to outer `<svg>`; transforms a `<g id="zoomlayer">`.
- Expose helpers: `zoomIn()`, `zoomOut()`, `resetView()`, `fitToFeature(feature)`.
- Persist transform in URL (`k,x,y`) and restore on load.

2) Hover (tooltip + focus)
- On `mousemove`: show tooltip near cursor; highlight boundary via stroke-weight bump.
- On `mouseleave`: hide tooltip.
- Tooltip content: `NNN Name · District` and current metric value (formatted).
- Debounce if needed for performance.

3) Legend
- Categorical (alliance): fixed swatch list from palette.
- Numeric:
  - `threshold/quantize/quantile`: stepped bins with labels (Indian formatted), include `NA`.
  - `sequential`: gradient bar with min–max labels.
- Optional: highlight legend bin on hover/selection.

4) Recoloring Pipeline
- On `metricId` or `classification` change:
  - Recompute scale from data distribution.
  - Update legend; update polygon `fill` only (do not recompute paths).
  - Preserve current zoom transform.

5) Search & Selection
- Search box: match AC number or case-insensitive substring of name; select + fit.
- Click on polygon or choose from dropdown → select, bring to front, center label at centroid.
- ARIA live region announces selection; keyboard support (+/−/0, Enter to select).

6) URL State & Embed
- Query params: `?metric=…&ac=…&k=…&x=…&y=…`.
- `history.replaceState` on interactions; parse on load.
- For iframe embeds, child posts height via `postMessage` when content changes.

7) Performance & Data
- Consider switching GeoJSON → TopoJSON for smaller payloads; compute `feature()` client-side.
- Precompute and cache centroids; avoid repeated `path.centroid` inside hot paths.

## Minimal API Sketch (future modularization)

```
initZoom(svg, layer, onEnd): { zoomIn, zoomOut, resetView, fitToFeature }
initHover(svg, layer, tooltipEl, formatter): void
renderLegend(container, scaleSpec, options): void
computeScale(values, classification, breaks): { type, scale }
colorForFeature(feature, scaleSpec, metric): string
```

## Coding Conventions

- Keep transforms on `<g id="zoomlayer">`; never mutate path coordinates.
- Recolor by updating `fill` only.
- All numeric formatting via Indian locale formatter.
- Accessibility first: ARIA live messages on selection; keyboard reachable controls.

## TODO (next iterations)

- [ ] Quantile/quantize legend labels tuned to exact bin ranges.
- [ ] Optional label decluttering for all-AC labels at higher zooms.
- [ ] Optional TopoJSON pipeline and boundary simplification.
- [ ] Parent/child embed scripts (postMessage height handshake) as standalone files.