# Metric Expansion Plan

## Context

- Primary viewer: `index_svg.html` (SVG + D3 v7).
- Data sources:
  - Boundaries: `bihar_ac_all.geojson` (FeatureCollection of AC polygons).
  - Attributes: `bihar_election_results_consolidated.csv` (joined by zero-padded `AC_NO` ? `no`).
  - Party metadata: `parties.json` (code ? alliance, name, color).
- Local helpers: `bihar_ac_geojson/` (per-AC files for other flows).

## Shared State & Metrics Roadmap

- `state`: `{ metricId, classification, breaks, zoomTransform, selectedKey }`.
- Planned metrics:
  - `alliance`: categorical (current/2020 combined), pastel palette for `{ NDA, MGB, OTH, NA }`.
  - `currentParty`: categorical; pastel palette generated from `parties.json` with fallbacks.
  - `reserved`: categorical (`GEN`, `SC`, `ST`, `NA`) with soft swatches.
  - Historical winners: `winnerParty15`, `winnerParty10`, `winnerAlliance15`, `winnerAlliance10` derived from CSV + party map.
  - Numeric: `margin20 | margin15 | margin10` for threshold/quantile/quantize.
- `scales` factory: `threshold | quantile | quantize | sequential`.
- Formatting: Indian locale (1,23,456) for legend/tooltip.

## Implementation Notes

- Fetch `parties.json` with the CSV before recoloring; only recolor once both datasets resolve.
- Pastelize party colors (e.g., mix toward white) for map readability.
- Legends should include a neutral "No data" swatch across categorical metrics.
- Persist `classification` in URL (`classify=` param) alongside existing state.
- Fix separator encoding upstream instead of post-replace.

## Follow-ups

- Quantile/quantize legend labels: use = / = ranges derived from scale thresholds.
- Sequential legend: render gradient bar + min/max labels.
- Cache `currentScaleSpec` per metric/classification change to avoid repeated computation.
- Consider TopoJSON pipeline and label decluttering in later passes.
