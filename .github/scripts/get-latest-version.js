// Finds the highest vMAJOR.MINOR.PATCH tag in the repository.
module.exports = async function getLatestVersion({ github, context }) {
  const { owner, repo } = context.repo;
  const tags = await github.paginate(github.rest.repos.listTags, { owner, repo, per_page: 100 });

  const versions = tags
    .map((t) => /^v(\d+)\.(\d+)\.(\d+)$/.exec(t.name))
    .filter(Boolean)
    .map((m) => ({ tag: m[0], parts: m.slice(1).map(Number) }))
    .sort((a, b) => a.parts[0] - b.parts[0] || a.parts[1] - b.parts[1] || a.parts[2] - b.parts[2]);

  return versions[versions.length - 1] || null;
};
