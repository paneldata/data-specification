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


@cli.command(short_help="Builds Tabular Data Package from config file")
@click.argument("config_file", type=click.Path(exists=True), default="config.yml")
@click.argument("datapackage_location", type=click.Path(), default="datapackage.json")
def build(config_file: str, datapackage_location: str) -> None:
    """Builds a Tabular Data Package from a configuration file.

    \b
    Args:
        config_file: The path to a configuration file.
        datapackage_location: The path to create the Tabular Data Package.

    """
    config = builder.read_yaml(pathlib.Path(config_file))
    package = builder.build(config)
    # package.save() writes with indent=4, so do not use it here.
    with open(str(datapackage_location), "w") as outfile:
        json.dump(package.descriptor, outfile, indent=2)


@cli.command(short_help="Infers a Tabular Data Package from directory")
@click.argument("metadata_directory", type=click.Path(exists=True))
@click.argument("datapackage_location", type=click.Path(), default="datapackage.json")
@click.option("--strict", is_flag=True, default=False)
def infer(
    metadata_directory: str, datapackage_location: str, strict: bool = False
) -> None:
    """Infers a Tabular Data Package from a given metadata directory.

    \b
    Args:
        metadata_directory: The path to a metadata directory.
        datapackage_location: The path to create the Tabular Data Package.
        strict: Use stricter rules (if available).

    """
    path = pathlib.Path(metadata_directory)
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


@cli.command(short_help="Validates Tabular Data Package or Data Resource")
@click.argument("datapackage_location", type=click.Path(exists=True))
@click.argument("resource_name", type=click.Path(), required=False)
@click.option("--check-relations", is_flag=True, default=False)
def validate(
    datapackage_location: str, resource_name: str, check_relations: bool = False
) -> None:
    """Validates a Tabular Data Package or a single Tabular Data Resource.

    \b
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


@cli.command(short_help="Validates dataset JSON files")
@click.argument("datasets_directory", type=click.Path(exists=True))
def validate_datasets(datasets_directory: str) -> None:
    """Validates dataset JSON files in datasets_location against JSON Schema.

    \b
    Args:
        datasets_directory: The path to a directory containing dataset JSON files.

    """
    validator.validate_files(datasets_directory, "datasets")


@cli.command(short_help="Validates instrument JSON files")
@click.argument("instruments_directory", type=click.Path(exists=True))
def validate_instruments(instruments_directory: str) -> None:
    """Validates instrument JSON files in instruments_directory against JSON Schema.

    \b
    Args:
        instruments_directory: The path to a directory containing instrument JSON files.

    """
    validator.validate_files(instruments_directory, "instruments")


if __name__ == "__main__":
    cli()
