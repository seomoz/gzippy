Gzippy
======

[![Build Status](https://travis-ci.org/seomoz/gzippy.svg?branch=master)](https://travis-ci.org/seomoz/gzippy)

Reading and writing gzip files, per [the RFC](http://www.zlib.org/rfc-gzip.html).

Goals
=====

- __Simplicity__ -- we've often found the batteries-included python gzip implementation to
    be more trouble than it's worth
- __Completeness__ -- most of the header information in the `gzip` container don't seem
    to be used very widely. All the same, this aims to make those fields accessible
- __Performance (eventually, if necessary)__ -- if at some point we feel it necessary, we
    may promote this to a C++ extension

Caveats
-------

- __Multiple members__ -- while the `gzip` container format describes how to add multiple
    members to an archive, this functionality is not included
- __Incremental reads__ -- currently three modes are supported: 1) incrementally reading
    chunks of data limited to a pre-determined size, 2) reading the lines of a file
    incrementally, or 3) reading the whole file in at once. The `read(<size>)` call,
    specifically is not yet supported.
- __Extra flags__ -- the `FEXTRA` field describes a list of pairs of
    `(subfield ID, field)`, and while it's made accessible (for both reading and writing),
    this does not include any utilities to easily format it.

Installation
============
`gzippy` is available on `pypi`:

```bash
pip install gzippy
```

Usage
=====
At the top-level, `gzippy` provides an `open` function much like `gzip`'s:

```python
import gzippy

with gzippy.open('example.gz', 'wb') as fout:
    fout.write('Some content.')

with gzippy.open('example.gz', 'rb') as fin:
    print(fin.read())
```

Reading data
------------
Data can be read all at once with a call to `read()`, or incrementally with a call to
the `chunks` generator (which reads chunks of a predetermined size from the compressed
file and yields decompressed blocks), or the `lines` generator (which yields lines):

```python
# Read it in all at once
with gzippy.open('smallish-archive.gz') as fin:
    data = fin.read()

# Read it in manageable chunks (on the order of 4KB)
with gzippy.open('really-big-archive.gz') as fin:
    for chunk in fin.chunks():
        ...

# Read it in line-by-line
with gzippy.open('really-big-archive.gz') as fin:
    # Alternatively, fin.lines()
    for line in fin:
        ...
```

Additional header information
-----------------------------
When writing a file, additional headers may be provided using the `GzipWriter` class
directly:

```python
with gzippy.GzipWriter.open('example.gz', name='example', comment='comment') as fout:
    ...
```

Similarly, these headers are available upon reading a file:

```python
with gzippy.open('example.gz') as fin:
    print(fin.headers)
```

Development
===========
It's recommended that you use a `virtualenv` to develop `gzippy`:

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Tests
=====
Tests are run with:

```bash
make test
```

PRs
===
These are not all hard-and-fast rules, but in general PRs have the following expectations:

- __pass Travis__ -- or more generally, whatever CI is used for the particular project
- __be a complete unit__ -- whether a bug fix or feature, it should appear as a complete
    unit before consideration.
- __maintain code coverage__ -- some projects may include code coverage requirements as
    part of the build as well
- __maintain the established style__ -- this means the existing style of established
    projects, the established conventions of the team for a given language on new
    projects, and the guidelines of the community of the relevant languages and
    frameworks.
- __include failing tests__ -- in the case of bugs, failing tests demonstrating the bug
    should be included as one commit, followed by a commit making the test succeed. This
    allows us to jump to a world with a bug included, and prove that our test in fact
    exercises the bug.
- __be reviewed by one or more developers__ -- not all feedback has to be accepted, but
    it should all be considered.
- __avoid 'addressed PR feedback' commits__ -- in general, PR feedback should be rebased
    back into the appropriate commits that introduced the change. In cases, where this
    is burdensome, PR feedback commits may be used but should still describe the changed
    contained therein.

PR reviews consider the design, organization, and functionality of the submitted code.

Commits
=======
Certain types of changes should be made in their own commits to improve readability. When
too many different types of changes happen simultaneous to a single commit, the purpose of
each change is muddled. By giving each commit a single logical purpose, it is implicitly
clear why changes in that commit took place.

- __updating / upgrading dependencies__ -- this is especially true for invocations like
    `bundle update` or `berks update`.
- __introducing a new dependency__ -- often preceeded by a commit updating existing
    dependencies, this should only include the changes for the new dependency.
- __refactoring__ -- these commits should preserve all the existing functionality and
    merely update how it's done.
- __utility components to be used by a new feature__ -- if introducing an auxiliary class
    in support of a subsequent commit, add this new class (and its tests) in its own
    commit.
- __config changes__ -- when adjusting configuration in isolation
- __formatting / whitespace commits__ -- when adjusting code only for stylistic purposes.

New Features
------------
Small new features (where small refers to the size and complexity of the change, not the
impact) are often introduced in a single commit. Larger features or components might be
built up piecewise, with each commit containing a single part of it (and its corresponding
tests).

Bug Fixes
---------
In general, bug fixes should come in two-commit pairs: a commit adding a failing test
demonstrating the bug, and a commit making that failing test pass.

Tagging and Versioning
======================
Whenever the version included in `setup.py` is changed (and it should be changed when
appropriate using [http://semver.org/](http://semver.org/)), a corresponding tag should
be created with the same version number (formatted `v<version>`).

```bash
git tag -a v0.1.0 -m 'Version 0.1.0

This release contains an initial working version of the `crawl` and `parse`
utilities.'

git push origin
```
