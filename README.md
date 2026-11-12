# inc00gnito.github.io

Personal CV website of Patrycja Kozak, live at https://inc00gnito.github.io/.

A static site built with plain HTML, CSS and JavaScript. No build step or dependencies.

## Structure

- `site/` - the website (`index.html`, `style.css`, `script.js`)
- `.github/workflows/pages.yml` - deploys `site/` to GitHub Pages

## Local preview

Open `site/index.html` in a browser.

## Deployment

Every push to `main` publishes the `site/` folder via GitHub Actions. This requires Settings > Pages > Source to be set to "GitHub Actions". The workflow can also be started manually from the Actions tab.
