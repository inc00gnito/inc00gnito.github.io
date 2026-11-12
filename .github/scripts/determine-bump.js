// Picks the bump level from Conventional Commit messages; the highest level wins.
//   type!: ... or BREAKING CHANGE: ...  -> major
//   feat: ...                           -> minor
//   anything else                       -> patch
module.exports = function determineBump(messages) {
  let bump = 'patch';
  for (const message of messages) {
    const subject = message.split('\n')[0];
    if (/^\w+(\([^)]*\))?!:/.test(subject) || /^BREAKING[ -]CHANGE:/m.test(message)) return 'major';
    if (/^feat(\([^)]*\))?:/.test(subject)) bump = 'minor';
  }
  return bump;
};
