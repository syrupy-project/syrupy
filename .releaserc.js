module.exports = {
    branch: "semantic-release",
    dryRun: true,
    plugins: [
        "@semantic-release/commit-analyzer",
        "@semantic-release/release-notes-generator",
        "@semantic-release/changelog",
        "@semantic-release/git",
        "@semantic-release/github",
    ],
};
