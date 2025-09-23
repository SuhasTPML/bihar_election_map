TopoJSON + Simplification Pipeline

Goal: shrink boundary payloads and speed up rendering by converting GeoJSON to TopoJSON with simplification and quantization.

Requirements
- Mapshaper CLI (recommended): https://github.com/mbloch/mapshaper
- Alternatively, Node topojson-server (for encoding) + topojson-client (for decoding in browser).

Using Mapshaper

1) Basic clean + simplify + quantize → TopoJSON

   mapshaper bihar_ac_all.geojson \
     -clean \
     -simplify visvalingam 12% keep-shapes \
     -o format=topojson quantization=1e5 bihar_ac_all.topojson

2) Keep only needed fields to reduce size further

   mapshaper bihar_ac_all.geojson \
     -clean \
     -keep-fields AC_NO,AC_NAME,DIST_NAME \
     -simplify visvalingam 12% keep-shapes \
     -o format=topojson quantization=1e5 bihar_ac_all.topojson

Notes
- Tune simplify percentage (8–18%) to balance fidelity vs size. Use keep-shapes to prevent topology collapse.
- quantization=1e5 is a good default for state-level maps; adjust if artifacts appear when zoomed.
- Ensure AC_NO/AC_NAME/DIST_NAME are preserved (names can vary in source; adapt the keep-fields list accordingly).

Browser Loader
- index_svg.html already attempts to load 'bihar_ac_all.topojson' first and falls back to 'bihar_ac_all.geojson'.
- Decoding uses topojson-client (via CDN) and picks the first object in the TopoJSON as the feature collection.

Validation Tips
- Visual diff before/after simplification using mapshaper GUI.
- Check bounding boxes and count of features (should remain 243 ACs).
- Verify the selection and tooltip properties match expected field names.

