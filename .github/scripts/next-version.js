// Applies a bump level to [major, minor, patch] and returns the new tag name.
module.exports = function nextVersion([major, minor, patch], bump) {
  if (bump === 'major') return `v${major + 1}.0.0`;
  if (bump === 'minor') return `v${major}.${minor + 1}.0`;
  return `v${major}.${minor}.${patch + 1}`;
};
