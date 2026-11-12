const getLatestVersion = require('./get-latest-version');
const getCommitMessages = require('./get-commit-messages');
const determineBump = require('./determine-bump');
const nextVersion = require('./next-version');
const createRelease = require('./create-release');

// Entry point used by .github/workflows/release.yml
module.exports = async function release({ github, context, core, bumpInput }) {
  const latest = await getLatestVersion({ github, context });

  let bump = bumpInput || 'auto';
  if (bump === 'auto') {
    const messages = await getCommitMessages({ github, context, lastTag: latest && latest.tag });
    bump = determineBump(messages);
  }

  const tag = nextVersion(latest ? latest.parts : [0, 0, 0], bump);
  await createRelease({ github, context, tag });
  core.info(`Released ${tag} (${bump} bump, previous: ${latest ? latest.tag : 'none'})`);
};
