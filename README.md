# data-specification

[![Issues][issues-badge]](https://github.com/paneldata/data-specification/issues/)
[![Travis][travis-badge]](https://travis-ci.org/paneldata/data-specification/)

## Installation

Install library from GitHub:

```shell
$ pip install git+https://github.com/paneldata/data-specification
```

Or using [pipenv](https://github.com/pypa/pipenv):

```shell
$ pip install --upgrade pipenv
$ pipenv shell
$ pipenv install git+https://github.com/paneldata/master@datapackage-directory#egg=ddionrails_datapackage
```

## Usage
```shell
# Build a datapackage.json for soep-core
$ git clone https://github.com/paneldata/data-specification.git
$ cd data-specification/
$ ddionrails-datapackage build examples/soep-core/config.yml
```

<!-- Markdown link & img dfn's -->
[travis-badge]: https://img.shields.io/travis/paneldata/data-specification.svg
[issues-badge]: https://img.shields.io/github/issues/paneldata/data-specification.svg