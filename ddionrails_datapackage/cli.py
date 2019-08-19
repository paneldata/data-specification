# -*- coding: utf-8 -*-
"""ddionrails datapackage CLI.

This module contains functions to build a Tabular Data Package from a configuration
dictionary.
"""

import json
import pathlib

import click
import pkg_resources
from datapackage import Package
from datapackage.exceptions import RelationError

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
@click.argument("metadata_location", type=click.Path(exists=True))
@click.argument("datapackage_location", type=click.Path(), default="datapackage.json")
@click.option("--strict", is_flag=True, default=False)
def infer(
    metadata_location: str, datapackage_location: str, strict: bool = False
) -> None:
    """Infers a Tabular Data Resource from a given metadata location.

    Args:
        metadata_location: The path to a metadata location.
        datapackage_location: The path to create the Tabular Data Package.
        strict: Use stricter rules (if available).

    """
    path = pathlib.Path(metadata_location)
    csv_files = [str(file.name) for file in sorted(path.glob("*.csv"))]
    if strict:
        including_strict = []
        for file in csv_files:
            path = pathlib.Path(file).stem
            strict_name = f"datapackage/resources/{path}_strict.yml"
            srict_path = pathlib.Path(
                pkg_resources.resource_filename("ddionrails_datapackage", strict_name)
            )
            if srict_path.exists():
                including_strict.append(srict_path.name)
            else:
                including_strict.append(file)
        csv_files = including_strict

    config = {"metadata": {}, "files": csv_files}
    package = builder.build(config)
    with open(str(datapackage_location), "w") as outfile:
        json.dump(package.descriptor, outfile, indent=2)


@cli.command()
@click.argument("datapackage_location", type=click.Path(exists=True))
@click.argument("resource_name", type=click.Path(), required=False)
@click.option("--check-relations", is_flag=True, default=False)
def validate(
    datapackage_location: str, resource_name: str, check_relations: bool = False
) -> None:
    """Validates a Tabular Data Package or a single Tabular Data Resource.

    Args:
        datapackage_location: The path to a Tabular Data Package.
        resource_name: The name of a single Tabular Data Resource to validate (optional).
        check_relations: Check relations for Tabular Data Resources (if available).

    """
    success = True
    package = Package(datapackage_location)
    if resource_name:
        to_validate = [resource_name]
    else:
        to_validate = [resource.name for resource in package.resources]
    for _resource_name in to_validate:
        report = validator.validate(datapackage_location, _resource_name)
        color = "green" if report["valid"] else "red"
        if color == "red":
            success = False
        click.secho(json.dumps(report, indent=2), fg=color)

        # only check relations, if validation status is "green"
        if check_relations and color == "green":
            resource = package.get_resource(_resource_name)
            try:
                resource.check_relations()
                click.secho("relation check passed", fg="green")
            except AttributeError:
                click.secho("relation check not passed", fg="red")
            except RelationError as error:
                click.secho(str(error), fg="red")

    if not success:
        exit(1)


if __name__ == "__main__":
    cli()
