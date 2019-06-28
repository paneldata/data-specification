# -*- coding: utf-8 -*-

import pathlib
from typing import Dict

import pkg_resources
import yaml
from datapackage import Package
from dpath.util import merge

DATAPACKAGE_BASE_FILE = pkg_resources.resource_filename(
    "ddionrails_datapackage", "datapackage/descriptor.yml"
)
DATAPACKAGE_BASE_RESOURCE = pkg_resources.resource_filename(
    "ddionrails_datapackage", "datapackage/resources/base.yml"
)
DATAPACKAGE_OUTFILE = pathlib.Path().cwd().joinpath("datapackage.json")


def read_yaml(filename: pathlib.Path) -> Dict:
    """ Reads a YAML file from disk and returns a Python dictionary """
    with open(str(filename), "r") as yaml_file:
        return yaml.safe_load(yaml_file)


def read_tabular_data_resource(resource_name: str) -> Dict:
    """ Reads a datapackage resource as YAML file from disk and returns a Python dictionary """
    base_resource = read_yaml(DATAPACKAGE_BASE_RESOURCE)
    filename = pkg_resources.resource_filename(
        "ddionrails_datapackage", f"datapackage/resources/{resource_name}.yml"
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
    wanted_files = [file.split(".")[0] for file in config["files"]]
    for file in wanted_files:
        if "_strict" in file:
            basic_file = file.replace("_strict", "")
            resource = read_tabular_data_resource(basic_file)
            strict_resource = read_tabular_data_resource(file)
            merge(resource, strict_resource)
        else:
            resource = read_tabular_data_resource(file)
        package.add_resource(resource)
    package.commit()
    if package.valid:
        package.save(target=DATAPACKAGE_OUTFILE)
    else:
        for error in package.errors:
            print(error)
