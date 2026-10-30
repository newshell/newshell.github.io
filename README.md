# codie / lab — engineering field notes

Public static website for https://blog.codie.uk, rebuilt in a technical lab-note style. No tracking script, external font CDN or author-profile auto-link.

## Architecture

GitHub Pages serves static HTML from repository root. Shared layout is implemented in compiled HTML, design tokens in `assets/site.css`, client interactions in `assets/site.js`. Illustrations are original SVG concept diagrams; only the historical NFC article uses an existing photograph.

## Edit / deploy

Edit the HTML under `blog/<slug>/index.html` and update `blog/index.html` plus `index.html` for new posts. Use a local static server for preview: `python -m http.server 8000`. Keep all existing URLs unchanged.

Before publishing: inspect the complete diff; verify local links, preserve `CNAME` and `assets/images/`, and follow `PRIVACY.md`. Nothing from a private repository is needed to build or deploy this site.
