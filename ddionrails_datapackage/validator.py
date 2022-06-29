# -*- coding: utf-8 -*-
"""ddionrails datapackage builder.

This module contains functions to validate a Tabular Data Resource in a given
Tabular Data Package.
"""

from typing import Dict

from datapackage import Package
from frictionless import validate as _validate


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
    return _validate(resource.source, schema=schema)
