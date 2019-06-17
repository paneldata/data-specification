# -*- coding: utf-8 -*-


import pathlib
from typing import Dict

import yaml

from datapackage import Package

DATAPACKAGE_DIRECTORY = pathlib.Path().cwd().joinpath("datapackage")
DATAPACKAGE_BASE_FILE = DATAPACKAGE_DIRECTORY.joinpath("descriptor.yml")
DATAPACKAGE_RESOURCES_DIRECTORY = DATAPACKAGE_DIRECTORY.joinpath("resources")
DATAPACKAGE_BASE_RESOURCE = DATAPACKAGE_RESOURCES_DIRECTORY.joinpath("base.yml")
DATAPACKAGE_OUTFILE = pathlib.Path().cwd().joinpath("datapackage.json")


def read_yaml(filename: pathlib.Path) -> Dict:
    """ Reads a YAML file from disk and returns a Python dictionary """
    with open(str(filename), "r") as yaml_file:
        return yaml.safe_load(yaml_file)


def read_tabular_data_resource(resource_name: str) -> Dict:
    """ Reads a datapackage resource as YAML file from disk and returns a Python dictionary """
    base_resource = read_yaml(DATAPACKAGE_BASE_RESOURCE)
    filename = DATAPACKAGE_RESOURCES_DIRECTORY.joinpath(resource_name).with_suffix(
        ".yml"
    )
    resource = read_yaml(filename)
    resource.update(base_resource)
    return resource


def build(config: Dict) -> None:
    """ Builds a Datapackage object from a config dictionary """

    # Read the descriptor base dictionary from disk and update it with values from the config file
    descriptor = read_yaml(DATAPACKAGE_BASE_FILE)
    descriptor["name"] = config["metadata"].get("name")
    descriptor["id"] = config["metadata"].get("id")
    descriptor["title"] = config["metadata"].get("title")
    # Remove empty keys from the dictionary
    descriptor = {key: value for key, value in descriptor.items() if value}

    # Create a Datapackage object from the descriptor dictionary
    package = Package(descriptor=descriptor)
    wanted_files = [
        file.split(".")[0] for file in config["files"] if config["files"][file] is True
    ]
    for file in wanted_files:
        resource = read_tabular_data_resource(file)
        package.add_resource(resource)
    package.commit()
    if package.valid:
        package.save(target=DATAPACKAGE_OUTFILE)
    else:
        for error in package.errors:
            print(error)
