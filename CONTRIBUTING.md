# How to contribute

**SAUCE** heavily uses the
[successful Git branching model](http://nvie.com/posts/a-successful-git-branching-model/)
by Vincent Driessen
([summary figure](http://nvie.com/files/Git-branching-model.pdf)).
His [git-flow extension](https://github.com/nvie/gitflow) makes it easier to employ this model.

**Please** just submit your *feature* branches for pull requests.

---

The following sections are mostly copied from https://github.com/puppetlabs/puppet/blob/master/CONTRIBUTING.md

---

## Getting Started

* If it's a bug or something worth discussing first, submit a ticket for your issue,
  assuming one does not already exist. You can skip that for simple new features
  since discussion can also happen on the pull request.
  * Clearly describe the issue including steps to reproduce when it is a bug.
  * Make sure you fill in the earliest version that you know has the issue.
* Fork the repository on GitHub

## Making Changes

* Create a *feature* branch (also called topic branch) from where you want to base your work
  (see the note on git-flow above).
  * This is usually the `develop` branch.
  * If you are certain your fix must be on a *release* branch, you should use a *hotfix* branch.
  * Please avoid working directly on the `develop` and `master` branches.
* Make commits of logical units.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure your commit messages are in the proper format.
* If you can, please add tests for your changes (even broken tests are better than no tests).

## Submitting Changes

* Push your changes to a feature branch in your fork of the repository.
* Submit a pull request to the repository.
