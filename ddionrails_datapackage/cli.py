# -*- coding: utf-8 -*-
"""ddionrails datapackage CLI.

This module contains functions to build a Tabular Data Package from a configuration
dictionary.
"""

import json
import pathlib

import click

from . import builder, validator


@click.group()
def cli() -> None:
    """ddionrails datapackage CLI"""


@cli.command()
@click.argument("config_file", type=click.Path(exists=True), default="config.yml")
@click.argument("datapackage_location", type=click.Path(), default="datapackage.json")
def build(config_file: str, datapackage_location: str) -> None:
    """Builds a Tabular Data Resource from a configuration file.

    Args:
        config_file: The path to a configuration file.
        datapackage_location: The path to create the Tabular Data Package.

    """
    config = builder.read_yaml(pathlib.Path(config_file))
    package = builder.build(config)
    # package.save() writes with indent=4, so do not use it here.
    with open(str(datapackage_location), "w") as outfile:
        json.dump(package.descriptor, outfile, indent=2)


@cli.command()
@click.argument("datapackage_location", type=click.Path(exists=True))
@click.argument("resource_location", type=click.Path(exists=True))
def validate(datapackage_location: str, resource_location: str) -> None:
    """Validates a single Tabular Data Resource.

    Args:
        datapackage_location: The path to a Tabular Data Package.
        resource_location: The path to a a file that should be validated.

    """
    report = validator.validate(datapackage_location, resource_location)
    color = "green" if report["valid"] else "red"
    click.secho(json.dumps(report, indent=2), fg=color)


if __name__ == "__main__":
    cli()
