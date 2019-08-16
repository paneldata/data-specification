# -*- coding: utf-8 -*-
"""ddionrails datapackage builder.

This module contains functions to validate a Tabular Data Resource in a given
Tabular Data Package.
"""

import pathlib
from typing import Dict

import goodtables.validate
from datapackage import Package


def validate(datapackage_location: str, resource_location: str) -> Dict:
    """Validates a single Tabular Data Resource.

    Args:
        datapackage_location: The path to a Tabular Data Package.
        resource_location: The path to a a file that should be validated.

    """
    resource_name = pathlib.Path(resource_location).stem
    datapackage = Package(datapackage_location)
    if resource_name not in datapackage.resource_names:
        message = (
            f"Resource '{resource_name}' unknown, try: {datapackage.resource_names}"
        )
        return {"message": message, "valid": False}
    resource = datapackage.get_resource(resource_name)
    schema = resource.schema.descriptor
    return goodtables.validate(resource_location, schema=schema, order_fields=True)
