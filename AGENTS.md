# Bihar Assembly Map — Choropleth Plan and Conventions

This document captures the design and implementation plan for the SVG/D3 choropleth (and a Leaflet variant where relevant). Refer to this when continuing work.

## Status (current)

- Implemented
  - Zoom (d3-zoom) with fit-to-feature; keyboard +/−/0; pan; URL state persistence.
  - Hover outline + tooltip (debounced) and legend bin highlight.
  - Legends: categorical (alliance swatches) and numeric (threshold/quantile/quantize/sequential gradient).
  - Metric selector and classification switch; recolor updates fill only.
  - Dropdown selection auto-zooms and shows CSV-backed details panel.
  - Close button shown on selection/zoom; resets selection and zoom.
  - Indian number formatting for legend/tooltip values.
  - URL params: metric, ac, k/x/y (shareable link) with restore on load.

- Pending
  - Fine-tune legend bin labels for quantile/quantize.
  - Optional label decluttering for all-AC labels at higher zooms.
  - Optional TopoJSON boundaries + simplification pipeline.
  - Optional parent/child embed scripts as standalone files.

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
  - `margin20 | margin15 | margin10`: numeric; derive from CSV columns.
- `scales` factory (based on `classification`): `threshold | quantile | quantize | sequential`.
- Number formatting: Indian locale (1,23,456) for legend/tooltip.

## Modules (SVG/D3)

1) Zoom (d3-zoom)
- Attach to outer `<svg>`; transform `<g id="zoomlayer">`.
- Helpers: `zoomIn()`, `zoomOut()`, `resetView()`, `fitToFeature(feature)`.
- Persist transform in URL (`k,x,y`) and restore on load.

2) Hover (tooltip + focus)
- On pointermove: show tooltip near cursor; draw hover outline above features.
- On pointerleave: hide tooltip and clear outline.
- Tooltip: `NNN Name · District` + current metric value (formatted).
- Debounce pointer tracking for smoothness.

3) Legend
- Categorical (alliance): fixed swatch list from palette.
- Numeric:
  - `threshold/quantize/quantile`: stepped bins with labels (Indian formatted), include `NA`.
  - `sequential`: gradient bar with min–max labels.
- Highlight legend bin on hover/selection.

4) Recoloring Pipeline
- On `metricId` or `classification` change:
  - Recompute scale from data distribution.
  - Update legend; update polygon `fill` only (no path recompute).
  - Preserve current zoom transform.

5) Selection & Details
- Dropdown and click select → bring to front, label at centroid, zoom to fit.
- Details panel shows MLA, party, alliance, margins (from CSV).
- ARIA live region announces selection; keyboard support (+/−/0, Enter to select).

6) URL State & Embed
- Query params: `?metric=…&ac=…&k=…&x=…&y=…`.
- `history.replaceState` on interactions; parse on load.
- For iframes, child can post height via `postMessage` when content changes (future module).

7) Performance & Data
- Consider switching GeoJSON → TopoJSON; compute `feature()` client‑side.
- Precompute/cache centroids; avoid repeated `path.centroid` in hot paths.

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
- Use Indian locale formatter for numbers.
- Accessibility: ARIA live messages; keyboard‑reachable controls.

## TODO (next iterations)

- [ ] Refine quantile/quantize legend labels (exact bounds).
- [ ] Optional label decluttering for all‑AC labels at higher zooms.
- [ ] Optional TopoJSON pipeline and boundary simplification.
- [ ] Optional parent/child embed scripts (postMessage height handshake).