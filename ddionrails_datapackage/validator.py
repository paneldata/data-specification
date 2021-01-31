# -*- coding: utf-8 -*-
"""ddionrails datapackage builder.

This module contains functions to validate a Tabular Data Resource in a given
Tabular Data Package.
"""

import json
import pathlib
from typing import Dict

import goodtables.validate
import jsonschema
import pkg_resources
from datapackage import Package


def validate(datapackage_location: str, resource_name: str) -> Dict:
    """Validates a single Tabular Data Resource.

    Args:
        datapackage_location: The path to a Tabular Data Package.
        resource_name: The name of a single Tabular Data Resource to validate.

    """
    datapackage = Package(datapackage_location)
    if resource_name not in datapackage.resource_names:
        message = f"Resource '{resource_name}' unknown, try: {datapackage.resource_names}"
        return {"message": message, "valid": False}
    resource = datapackage.get_resource(resource_name)
    schema = resource.schema.descriptor
    return goodtables.validate(
        resource.source, schema=schema, order_fields=True, row_limit=-1
    )


def validate_files(directory: str, schema_file: str) -> None:
    """Validates JSON files against a JSON Schema.

    Args:
        directory: The path to a directory containing JSON files.
        schema_file: The schema file to validate against.

    """
    files = pathlib.Path(directory).glob("*.json")
    schema_location = pkg_resources.resource_filename(
        "ddionrails_datapackage", f"jsonschema/{schema_file}.json"
    )
    with open(schema_location, "r") as infile:
        schema = json.load(infile)
    for filename in files:
        with open(str(filename), "r") as infile:
            dataset = json.load(infile)
        jsonschema.validate(dataset, schema)


def validate_datasets(directory: str) -> None:
    """Validates dataset JSON files against a JSON Schema.

    Args:
        directory: The path to a directory containing dataset JSON files.

    """
    validate_files(directory, "datasets")


def validate_instruments(directory: str) -> None:
    """Validates instrument JSON files against a JSON Schema.

    Args:
        directory: The path to a directory containing instrument JSON files.

    """
    validate_files(directory, "instruments")
