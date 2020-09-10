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
$ pipenv install git+https://github.com/paneldata/data-specification@master#egg=ddionrails_datapackage
```

## Usage

### Build a datapackage from a configuration file.

```shell
# Build a datapackage.json for soep-core
$ git clone https://github.com/paneldata/data-specification.git
$ cd data-specification/
$ ddionrails-datapackage build examples/soep-core/config.yml
```

### Infer a datapackage from a directory containing metadata files.

```shell
# creates a file called datapackage.json in the current directory
$ ddionrails-datapackage infer metadata-directory
```

```shell
$ cd metadata-directory/
$ ddionrails-datapackage infer .
```

```shell
# providing a filename for the datapackage is possible
$ ddionrails-datapackage infer metadata-directory something-different.json
```

```shell
# try to use strict rules for all discovered metadata files
$ ddionrails-datapackage infer metadata-directory --strict
```

### Validation

```shell
$ cd metadata-directory/
```

```shell
# validates all resources that are defined in datapackage.json
$ ddionrails-datapackage validate datapackage.json
```

```shell
# validates all resources that are defined in datapackage.json, including relationships
$ ddionrails-datapackage validate datapackage.json --check-relations
```

```shell
# validates "variables" resource that is defined in datapackage.json
$ ddionrails-datapackage validate datapackage.json variables
```

```shell
# validates "variables" resource that is defined in datapackage.json, including relationships
$ ddionrails-datapackage validate datapackage.json variables --check-relations
```


<!-- Markdown link & img dfn's -->
[travis-badge]: https://img.shields.io/travis/paneldata/data-specification.svg
[issues-badge]: https://img.shields.io/github/issues/paneldata/data-specification.svg
