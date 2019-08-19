# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,redefined-outer-name
"""Test cases for validator.py"""

from ddionrails_datapackage import validator


def test_validate_valid():
    datapackage_location = "tests/data/valid-resource/datapackage.json"
    resource_name = "variables"
    result = validator.validate(datapackage_location, resource_name)
    assert result["valid"]


def test_validate_invalid():
    resource_name = "variables"
    datapackage_location = "tests/data/invalid-resource/datapackage.json"
    result = validator.validate(datapackage_location, resource_name)
    assert not result["valid"]


def test_validate_invalid_resource_name():
    datapackage_location = "tests/data/valid-resource/datapackage.json"
    resource_name = "invalid-resource"
    result = validator.validate(datapackage_location, resource_name)
    assert not result["valid"]
    assert "unknown" in result["message"]
