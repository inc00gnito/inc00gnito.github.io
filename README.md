# inc00gnito.github.io

Personal CV website of Patrycja Kozak, live at https://inc00gnito.github.io/.

A static site built with plain HTML, CSS and JavaScript. The CV sections are rendered from `cv-data/` by a small Python script during deployment.

## Structure

- `site/` - the website (`index.html`, `style.css`, `script.js`)
- `cv-data/` - CV knowledge base in YAML; the site's CV sections are generated from it (see its README)
- `tools/build_site.py` - renders `cv-data/` into `site/index.html` during deployment
- `.github/workflows/pages.yml` - deploys `site/` to GitHub Pages

## Local preview

Open `site/index.html` in a browser.

## Deployment

Every push to `main` runs `tools/build_site.py` and then publishes the `site/` folder via GitHub Actions. This requires Settings > Pages > Source to be set to "GitHub Actions". The workflow can also be started manually from the Actions tab.
