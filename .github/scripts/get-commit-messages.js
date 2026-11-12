// Returns the commit messages that will be part of the new release.
// With no previous tag, only the head commit is considered.
module.exports = async function getCommitMessages({ github, context, lastTag }) {
  const { owner, repo } = context.repo;

  if (!lastTag) {
    const { data } = await github.rest.repos.getCommit({ owner, repo, ref: context.sha });
    return [data.commit.message];
  }

  const { data } = await github.rest.repos.compareCommitsWithBasehead({
    owner,
    repo,
    basehead: `${lastTag}...${context.sha}`,
    per_page: 100,
  });
  return data.commits.map((c) => c.commit.message);
};
