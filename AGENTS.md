# Agent Context

Personal collection of small browser-based tools, published via GitHub Pages
at https://4toddt.github.io/tools/. Each tool is its own folder with a
self-contained `index.html`.

The repo and its Pages site are public. Work tools and company data don't
belong here: La-Z-Boy tool pages live in the private `dev` repo under
`dev/tools/` and are served from UAT XM (see
`docs/reference/tools/tools-pages.md` in the monorepo).

## Conventions
- Vanilla HTML/CSS/JS, system fonts
- No build step, no package manager
- External CDN deps avoided when possible; when used, pin with SRI hash
- Root `index.html` lists all tools

## Still to move out

`bcc-cover-sku-reconciliation/` holds La-Z-Boy work notes plus BCC exports and
Merchandising cover workbooks. Its own note says to delete it after the first
BCC cover import is verified.
