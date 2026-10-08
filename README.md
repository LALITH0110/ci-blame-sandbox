# ci-blame-sandbox

Scratch repo for testing the Vecna CI-blame goal. The `PR` workflow runs the
unit tests on every push to `dev`.

- Red: merge a PR into `dev` that breaks a function, e.g. make `add` return `a - b`.
- Green: merge a PR that fixes it.

Merge PRs with squash so each commit on `dev` is one PR.

## Running tests

`python -m unittest discover -s tests -v`
