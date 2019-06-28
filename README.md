# data-specification

## Installation

Install library directly from GitHub with [pipenv](https://github.com/pypa/pipenv).

```shell
$ pip install --upgrade pipenv
$ pipenv shell
$ pipenv install git+https://github.com/paneldata/data-specification@datapackage-directory#egg=ddionrails_datapackage
```

## Usage
```shell
# Build a datapackage.json for soep-core
$ git clone https://github.com/paneldata/data-specification.git
$ ddionrails-datapackage build examples/soep-core/config.yml
```