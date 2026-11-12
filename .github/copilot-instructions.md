# Copilot instructions

## Commit messages and releases

Releases are automated (`.github/workflows/release.yml`, logic in `.github/scripts/`). The version bump is derived from [Conventional Commits](https://www.conventionalcommits.org/) messages since the last tag, so always write commit messages (and squash-merge PR titles) in this format:

- `feat: ...` - new feature or content, bumps **minor**
- `fix: ...` - bug fix, bumps **patch**
- `docs:`, `chore:`, `refactor:`, `style:`, `ci:` etc. - bump **patch**
- `feat!: ...` (any type with `!`) or a `BREAKING CHANGE:` footer - bumps **major**

The highest level among the commits wins. To change the rules, edit `.github/scripts/determine-bump.js` and keep this file and the README "Releases" section in sync.
