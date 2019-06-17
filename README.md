# data-specification

```shell
# Setup dependencies
$ https://github.com/paneldata/data-specification.git
$ cd data-specification/
$ pip install --upgrade pipenv
...
Successfully installed pipenv-2018.11.26 virtualenv-clone-0.5.3
$ pipenv install --dev
Installing dependencies from Pipfile.lock (e3b13d)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 56/56 — 00:00:05
$ pipenv shell
```

```shell
# Build a datapackage.json for soep-core
(data-specification) $ python cli.py build examples/soep-core/config.yml
```