# Bihar Map Enhancement Plan

## Project Overview
Working with Bihar Assembly constituency map visualization. Two main files:
- `index_svg_first.html` - Simple, working version with CSS-only hover (243 lines)
- `index.html` - Complex choropleth version with hover issues due to overlapping geometries (654 lines)

## Issue Identified
The complex version has JavaScript hover event listeners that trigger on overlapping geometries, causing constituencies 001, 002, etc. to interfere with hover events on other constituencies. The simple version uses CSS-only hover which works cleanly.

## Approved Enhancement Plan

### Phase 1: Button Consolidation
- Remove `#clearSel` and `#resetView` buttons from HTML
- Create single `clearAndReset()` function combining both actions:
  - Clear selection (`selectedId = null`)
  - Remove labels (`labelLayer.selectAll('*').remove()`)
  - Zoom to identity (`svg.transition().call(zoom.transform, d3.zoomIdentity)`)
  - Reset dropdown (`selEl.value = ''`)
  - Disable export (`exportSel.disabled = true`)
- Keep existing zoom in/out buttons unchanged

### Phase 2: Minimal Cross Button
- Add simple X button in SVG top-right corner using `ui.append('g')`
- Position: `translate(${width - 30}, 30)`
- Style: White circle with dark X lines
- Show/hide logic: Only visible when `selectedId !== null` or zoom scale > 1
- Action: Calls `clearAndReset()` on click
- Keyboard accessible (Enter/Space)

### Phase 3: Basic Searchable Dropdown
- Replace `<select id="acSelect">` with:
  ```html
  <input id="acSearch" type="search" placeholder="Search constituency..." list="acList" />
  <datalist id="acList"></datalist>
  ```
- Keep same data population in `populateSelect()` function
- Add search event listener for type-to-search functionality
- No complex filtering - use browser's native datalist matching

## Implementation Guidelines
- **Minimal code changes**: Target ~30 lines total
- **Keep file lightweight**: Final size ~270 lines
- **Preserve functionality**: All existing features maintained
- **No heavy CSS**: Simple, clean styling only
- **Avoid complexity**: No state management or animations beyond existing

## Key Principle
Maintain the working CSS-only hover system from `index_svg_first.html` to avoid geometry overlap issues while adding modern UI enhancements.

## Files to Modify
- `index_svg_first.html` - Apply enhancements here (working base)
- Do NOT modify `index.html` - keep as reference for advanced features

## Success Criteria
- Clean hover behavior (no ghost events)
- Intuitive single-action reset
- Searchable constituency selection
- Minimal, maintainable code