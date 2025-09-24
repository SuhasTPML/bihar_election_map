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
    - Attributes:  (joined by zero-padded  ↔ ).
  - Party metadata:  (code → alliance, name, color).
- Local helpers created earlier:  (per-AC files for other flows).

## Shared State and Configuration

- : .
-  roadmap:
  - : categorical (current/2020 combined), pastel palette for .
  - : categorical; palette generated from  pastelized colors with graceful fallback.
  - : categorical (, , , ) with soft swatches.
  - Historical: , , ,  derived from CSV + party map.
  - Margins:  numeric columns for threshold/quantile modes.
-  factory (based on ): .
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
- [ ] Optional label decluttering for all-AC labels at higher zooms.
- [ ] Optional TopoJSON pipeline and boundary simplification.
- [ ] Optional parent/child embed scripts (postMessage height handshake).

## Review & Improvements (index_svg.html)

### What Works
- Smooth zoom/pan with fit-to-feature and URL k/x/y restore.
- Hover outline + tooltip; categorical/numeric color modes and legend update.
- Metric/classification controls; Indian number formatting.
- Selection zoom and CSV-backed details panel.

### Bugs / Breakages
- Classification mode is not persisted to the URL ( parameter missing).
- Misencoded separator still surfaces as  in info/details; replace upstream rather than via string patch.

### UX Improvements
- Add search (with `datalist`) for quick AC lookup; dropdown alone is heavy.
- Persist `classification` in URL (e.g., `classify=quantile`) for fully shareable links.
- Add visible “Reset/Home” control and small keyboard hints (+/−/0).
- On selection, keep a pinned label near centroid and mirror tooltip data in details panel.
- Touch: treat tap as select and suppress hover tooltip on touch pointers.

### Legend / Classification
- Add an explicit "No data" swatch/color in legend and map (e.g., ).
- Switch categorical palettes to pastel variants (party/alliance/reserved) so the map stays readable.
- For , derive bin labels from scale thresholds with clear bounds (≤ a, a–b, ≥ b).
- Render the sequential legend as a visible gradient bar with min-max labels; size  boxes in CSS.
- Cache and reuse the computed numeric scale; avoid recompute per feature.

### Accessibility
- Give `<svg>` an `aria-label` describing the current metric.
- Make each AC keyboard-focusable/selectable (Enter) and apply focus outline.
- Keep ARIA live announcement; ensure control order is logical for tabbing.

### Performance / Data
- Cache  on metric/classification change and reuse in  and legend highlight.
- Consider TopoJSON + simplification for production to reduce payload size.
- Delay recolor until CSV +  both resolve to avoid redundant updates.

### Embed / Share
- Add `postMessage` hook to send height changes to parent on selection/legend change.
- Copy link should include `metric`, `classify`, `ac`, and `k/x/y`; show a brief toast.

### Quick Fixes (Code Pointers)
- Implement `clearSelection()`:
  - Clear `selectedId`, remove `.selected`, clear label/details/info, reset zoom (`zoom.transform` to identity), update URL, hide Close.
- Wire AC dropdown:
  - `selEl.addEventListener('change', e => e.target.value ? selectByKey(e.target.value) : clearSelection());`
- Cache scale:
  - `let currentScaleSpec = null;` Set in `updateLegendAndRecolor()` via `computeValueMap()` and reuse in `colorForFeature`/legend highlight.
- Legend CSS sizing:
  - `.legend .swatch { display:inline-block; width:12px; height:12px; border:1px solid #ccc; margin-right:4px; }`
  - `.legend .gradient { width:160px; height:10px; background: linear-gradient(to right, #f2f0f7, #54278f); border:1px solid #ccc; }`
- URL param:
  - Read/write `classify` in `applyViewFromURL()`/`pushURLState()`.
