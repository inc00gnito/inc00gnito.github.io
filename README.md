# inc00gnito.github.io

**🌐 Live site:** [**inc00gnito.github.io**](https://inc00gnito.github.io/)

A static site built with plain HTML, CSS and JavaScript. 
The CV sections are rendered from `cv-data/` by a small Python script during deployment.

## Structure

- `site/` - the website (`index.html`, `style.css`, `script.js`)
- `cv-data/` - CV knowledge base in YAML; the site's CV sections are generated from it (see its README)
- `tools/build_site.py` - renders `cv-data/` into `site/index.html` during deployment
- `.github/agents/cv-assistant.agent.md` - Copilot agent that maintains `cv-data/` and builds tailored CVs
- `.github/workflows/pages.yml` - deploys `site/` to GitHub Pages
- `.github/workflows/release.yml` - auto-tags and creates GitHub Releases (logic lives in `.github/scripts/`, one script per step)

## Updating the CV

1. Run the `cv-assistant` agent in **interactive** mode (`copilot --agent cv-assistant`, or `/agent` in a session). It interviews you about new work, tools and skills, then updates only `cv-data/`. Autopilot won't work because it needs your answers.
2. Optional: ask it for a tailored CV from a job posting; the result is written to `out/` (git-ignored).
3. Commit and push. GitHub Actions regenerates the site sections from `cv-data/` on deploy.

The agent never edits `site/` and only runs the preview when asked.

## Local preview

Preview the generated site without touching `site/` (needs `pip install pyyaml`):

```
python tools/build_site.py --preview
```

Other flags: `--dry-run` prints the diff, `--check` exits 1 if `site/index.html` is out of date, `--no-open` skips opening the browser. Plain `python tools/build_site.py` writes the result into `site/index.html`. Opening `site/index.html` directly shows the last generated version.

## Deployment

Every push to `main` runs `tools/build_site.py` and then publishes the `site/` folder via GitHub Actions. This requires Settings > Pages > Source to be set to "GitHub Actions". The workflow can also be started manually from the Actions tab.

## Releases

Every push to `main` also runs `.github/workflows/release.yml`, which creates the next `vMAJOR.MINOR.PATCH` tag and a GitHub Release with auto-generated notes. The default is a patch bump, detected from [Conventional Commits](https://www.conventionalcommits.org/) messages since the last tag: `feat:` bumps minor, `fix:` (or anything else) bumps patch, and `type!:` or a `BREAKING CHANGE:` footer bumps major. The highest level wins. You can also run the workflow manually and pick the bump. The first release is `v0.0.1`.
