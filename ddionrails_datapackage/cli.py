# -*- coding: utf-8 -*-

import json
import pathlib

import click

from . import builder, validator


@click.group()
def cli():
    pass


@cli.command()
@click.argument("config_file", type=click.Path(exists=True), default="config.yml")
def build(config_file: str):
    config = builder.read_yaml(pathlib.Path(config_file))
    builder.build(config)


@cli.command()
@click.argument("datapackage_location", type=click.Path(exists=True))
@click.argument("resource_location", type=click.Path(exists=True))
def validate(datapackage_location: str, resource_location: str):
    report = validator.validate(datapackage_location, resource_location)
    color = "green" if report["valid"] else "red"
    click.secho(json.dumps(report, indent=2), fg=color)


if __name__ == "__main__":
    cli()
