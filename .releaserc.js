module.exports = {
    plugins: [
        "@semantic-release/commit-analyzer",
        "@semantic-release/release-notes-generator",
        [
            "@semantic-release/changelog",
            {
                changelogTitle:
                    "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\nThe format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).\n\nFrom v1.0.0 onwards, this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Pre-v1, breaking changes will be indicated via a minor release, while all other changes will fall under patches. At any time, you can see what's in progress for a version by filtering GitHub issues by milestone.",
            },
        ],
        ["@semantic-release/git", { assets: ["CHANGELOG.md"] }],
        "@semantic-release/github",
    ],
};
