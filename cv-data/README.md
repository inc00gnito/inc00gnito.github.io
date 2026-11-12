# CV knowledge base

Everything about my career in one place. The YAML itself is not published, but the website is built from it (see below). When building a CV, pick and trim from here.

| File | Contents |
| --- | --- |
| `profile.yml` | Name, headline, summary variants, contact, spoken languages |
| `experience.yml` | Employers → roles → achievements |
| `skills.yml` | Skills grouped by area |
| `certifications.yml` | Certifications by issuer |
| `education.yml` | Degrees |
| `projects.yml` | Side projects, talks, open source (template) |

## Generating a CV and updating the data

Use the `cv-assistant` agent (`.github/agents/cv-assistant.agent.md`, available in Copilot CLI via `/agent` or `--agent cv-assistant`, and in VS Code Copilot Chat). Tell it about new work ("I just finished X, did Y, tools Z") or just mention a tool or skill, and it interviews you about real work experience before updating these files. It only edits `cv-data/` and `out/`, never `site/`, and only runs the site preview when you ask. Paste a job posting and it selects from them and writes `out/cv-<role>.md` (git-ignored).

## The website

GitHub Actions runs `tools/build_site.py` on every deploy. It renders About, "Currently", Experience, Skills, Certifications and Education & Languages into `site/index.html`, between the `<!-- cv:NAME -->` markers. Don't hand-edit inside those markers; edit the YAML instead. Everything else in the HTML (nav, hero, marquee, terminal, contact) stays hand-edited.

- Achievements with `text` appear on the site; set `site: false` to keep one (or a skill, certification, role) off it.
- To preview locally: `pip install pyyaml`, then `python tools/build_site.py --preview`. It builds a copy of the site in `out/preview/` (git-ignored) with your YAML changes applied and opens it in the browser; `site/` is not touched. Add `--no-open` to skip opening the browser. `--dry-run` prints the diff instead. Running with no flag writes `site/index.html` (`git restore site/index.html` undoes it), and `--check` tests whether the HTML is out of date.

## Conventions

- Dates are `YYYY-MM`; use `end: present` for current roles.
- Each achievement has a unique `id`, a `title`, a `text` and `tags` for filtering. Optional: `metrics`, `tech`.
- Polished `text` is optional. Jot rough `facts` (bullets, messy is fine) and have Copilot write the wording when building a CV. Once you like a phrasing, paste it into `text` to reuse it.
- Keep adding detail here even if it is too long for a CV; trim when writing the CV.
- Empty fields are prompts for things to fill in later.
