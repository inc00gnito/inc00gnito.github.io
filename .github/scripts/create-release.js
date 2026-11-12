// Creates the tag (at the triggering commit) and a GitHub Release with generated notes.
module.exports = async function createRelease({ github, context, tag }) {
  const { owner, repo } = context.repo;
  await github.rest.repos.createRelease({
    owner,
    repo,
    tag_name: tag,
    target_commitish: context.sha,
    name: tag,
    generate_release_notes: true,
  });
};
