# -*- coding: utf-8 -*-

import pathlib

import click

import datapackage_builder


@click.group()
def cli():
    pass


@cli.command()
@click.argument("config_file", type=click.Path(exists=True), default="config.yml")
def build(config_file: str):
    config = datapackage_builder.read_yaml(pathlib.Path(config_file))
    datapackage_builder.build(config)


if __name__ == "__main__":
    cli()
