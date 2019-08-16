# -*- coding: utf-8 -*-
"""ddionrails datapackage builder.

This module contains functions to build a Tabular Data Package from a configuration
dictionary.
"""

import logging
import pathlib
from typing import Dict

import pkg_resources
import yaml
from datapackage import Package
from dpath.util import merge

LOGGER = logging.getLogger(__name__)

DATAPACKAGE_BASE_FILE = pkg_resources.resource_filename(
    "ddionrails_datapackage", "datapackage/descriptor.yml"
)
DATAPACKAGE_BASE_RESOURCE = pkg_resources.resource_filename(
    "ddionrails_datapackage", "datapackage/resources/base.yml"
)


def read_yaml(filename: pathlib.Path) -> Dict:
    """Reads a YAML file from disk.

    Args:
        filename: The filename to be read from disk.

    Returns:
        The contents of "filename" as a dictionary.

    """
    with open(str(filename), "r") as yaml_file:
        return yaml.safe_load(yaml_file)


def read_tabular_data_resource(resource_name: str) -> Dict:
    """Reads a Tabular Data Resource from disk.

    Args:
        resource_name: The name of the Tabular Data Resource to be created.

    Returns:
        A Tabular Data Resource as a dictionary.

    """
    base_resource = read_yaml(DATAPACKAGE_BASE_RESOURCE)
    filename = pkg_resources.resource_filename(
        "ddionrails_datapackage", f"datapackage/resources/{resource_name}.yml"
    )
    resource = read_yaml(filename)
    resource.update(base_resource)
    return resource


def build(config: Dict) -> Package:
    """Builds a datapackage.Datapackage object from a config dictionary.

    The configuration dictionary should contain the following keys:
    "metadata", "files".

    Information about the corresponding study can be placed in metadata.
    Example:
        {
            'metadata': {
                'name': 'ddionrails-study',
                'id': 'doi'
            }
        }
    The desired files to be included in the Tabular Data Package can be placed in 'files':
    Example:
        {
            'files': [
                'concepts.csv'
            ]
        }

    See: examples/example-config.yml

    The resulting Tabular Data Package is written to disk as 'datapackage.json' in
    the directory the command line tool is run.

    Args:
        config: The configuration of the Datapackage to be created.

    """

    if "metadata" not in config or "files" not in config:
        raise ValueError("Config must contain 'metadata' and 'files'")

    # Read the descriptor base dictionary from disk
    # and update it with values from the config file
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
        # If a filename ends with "_strict"
        # create the basic Tabular Data Resource first
        # then add the "stricter" rules from the "_strict" file
        if "_strict" in file:
            basic_file = file.replace("_strict", "")
            resource = read_tabular_data_resource(basic_file)
            strict_resource = read_tabular_data_resource(file)
            merge(resource, strict_resource)
        else:
            resource = read_tabular_data_resource(file)
        package.add_resource(resource)
    package.commit()
    if not package.valid:
        for error in package.errors:
            LOGGER.error(error)
    return package
