---
title: Contribute to Turktools
layout: default
---

## Design goals

turktools is designed with the non-technical user in mind. Therefore, the following principles are adopted in its design and development:

* **Be portable**: each tool is a stand-alone script, and can be moved or copied to a different filesystem location and continue to function.
* **Be graceful**: catch failures and present useful warnings and errors to the user.
* **No dependencies**: just Python, out of the box.

The current development target is Python 2.6 and 2.7. Python 3 support [would be great in the future](https://github.com/mitcho/turktools/issues/3).

Note that an unfortunate consequence of the portability goal is to explicitly eschew a shared code library, forcing code duplication across different scripts, in violation of [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself). The current approach is to at least ensure the integrity of duplicated code across tools, by subjecting them to the exact same [tests](#testing). (Perhaps a build tool will be used in the future to cut down on such redundancies.) Note also that the no dependencies goal and Python 2.6 target means that nice libraries like `argparse` cannot be used.

## Contributing

Contributions are welcome! Bug reports, feedback, documentation improvements, and code changes are all welcome forms of contributions. Thank you (in advance) for making *turktools* better for everyone.

### Bug reports and feature requests:

New bug reports and feature requests can be added [on the turktools issue tracker](https://github.com/mitcho/turktools/issues?state=open). Please check whether your issue is already reported by someone else before opening a new issue. You must be logged into GitHub to create an issue.

### Code:

turktools is developed [on GitHub](https://github.com/mitcho/turktools). The best way to hack on turktools is to open a GitHub account, [*fork* this repository](https://help.github.com/articles/fork-a-repo), and modify your own "fork" of the turktools. To submit changes, you can then initiate a [*pull request*](https://help.github.com/articles/using-pull-requests). Within reason, pull requests should include new [test cases](#testing), in order to avoid later regressions.

Contributors should be familiar with the [technical design goals](#design-goals) above.

### Documentation:

[The turktools website](http://turktools.net) is where we post additional documentation. The code for this site is [on the `gh-pages` branch of our GitHub repository](https://github.com/mitcho/turktools/tree/gh-pages) and therefore can be edited via pull request, described above. Feel free to contribute any materials there that you think may be helpful to a broader audience.

## Testing

[![Test Status](https://travis-ci.org/mitcho/turktools.png?branch=master)](https://travis-ci.org/mitcho/turktools)

turktools includes unit tests using the Python-standard `unittest` library. Tests can be run by running `python tests.py`. With the [`coverage`](http://nedbatchelder.com/code/coverage/) module installed, run `coverage run tests.py` and then use `coverage report -m` to see a code coverage report.
