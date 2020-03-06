# Contributing

:tada: Thanks for taking the time to contribute! :tada:

The following is a set of guidelines for contributing to [syrupy](https://github.com/tophat/syrupy).

These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document.

## Table Of Contents

[Code of Conduct](#code-of-conduct)

[What should I know before I get started?](#what-should-i-know-before-i-get-started)

- [Python 3](#python-3)
- [Snapshot Testing](#snapshot-testing)
- [Releases](#releases)

[How Can I Contribute?](#how-can-i-contribute)

- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Pull Requests](#pull-requests)

[Styleguides](#styleguides)

- [Commit Messages](#commit-messages)
- [Code Styleguide](#code-styleguide)
- [`pathlib` over `os.path`](#usage-of-pathlib)

[Additional Notes](#additional-notes)

- [Issue and Pull Request Labels](#issue-and-pull-request-labels)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## What should I know before I get started

### Python 3

- Python typing and hints: [typing](https://docs.python.org/3/library/typing.html)

### Snapshot Testing

- Javascript snapshot testing [jest](https://jestjs.io/docs/en/snapshot-testing)

### Releases

- Semantic versioning: [semver](https://semver.org/spec/v2.0.0.html)

## How Can I Contribute

Before diving into writing code, please take a look at the following.

### Reporting Bugs

When attempting to fix a bug, create an issue using the "Bug report" template.

Give as much information in this issue as it allows for discussions and documentation about the decisions reached for any bugs that have been encounted.

### Suggesting Enhancements

Have an idea? Create an issue using the "Feature request" template.

Detailing in there as much as possible, the idea and any potential solutions to it, before suggesting a pull request.

### Your First Code Contribution

Have an issue to submit code changes for? See below.

#### Local development

- Clone the repository
- Run `. script/bootstrap` to ensure you're working from the correct environment
  - Ensure you do not have syrupy installed locally by running `pip uninstall syrupy -y`
- Run `inv test -d` to verify enviroment is correctly setup
  - The `-d` flag uses the development version of syrupy in `./src`
- Checkout a new branch and add code changes
- Add tests to verify code changes and rerun `inv test -d`
- See submitting [pull requests](#pull-requests)

### Pull Requests

Creating a pull request uses our template using the GitHub web interface.

Fill in the relevant sections, clearly linking the issue the change is attemping to resolve.

## Styleguides

### Commit Messages

Provide semantic commit messages following this [convention](https://www.conventionalcommits.org/en/v1.0.0/#summary).
This informs the semantic versioning we use to control our [releases](#releases).

### Code Styleguide

A linter is available to catch most of our styling concerns.
This is provided in a pre-commit hook when setting up [local development](#local-development).

You can also run `inv lint --fix` to see and solve what issues it can.

### Usage of Pathlib

`pathlib` is the preferred library when dealing with path operations. Some [documentation](https://docs.python.org/3/library/pathlib.html#correspondence-to-tools-in-the-os-module) is available to help translate `os.path`-type calls to `pathlib` calls. Documentation on `pathlib`'s API is also available on the same page.

## Additional Notes

### Issue and Pull Request Labels

Please tag issues and pull requests according to the relevant [github labels](https://github.com/tophat/syrupy/issues/labels).
