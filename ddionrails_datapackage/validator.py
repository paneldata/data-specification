# -*- coding: utf-8 -*-

import pathlib

import goodtables.validate
from datapackage import Package


def validate(datapackage_location: str, resource_location: str):
    resource_name = pathlib.Path(resource_location).stem
    datapackage = Package(datapackage_location)
    if resource_name not in datapackage.resource_names:
        return {
            "message": f"Resource '{resource_name}' is unknown, try: {datapackage.resource_names}",
            "valid": False,
        }
    resource = datapackage.get_resource(resource_name)
    schema = resource.schema.descriptor
    return goodtables.validate(resource_location, schema=schema, order_fields=True)
