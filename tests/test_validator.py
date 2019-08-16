# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,redefined-outer-name
"""Test cases for validator.py"""

from ddionrails_datapackage import validator


def test_validate_valid():
    datapackage_location = "tests/data/datapackage.json"
    resource_location = "tests/data/valid/variables.csv"
    result = validator.validate(datapackage_location, resource_location)
    assert result["valid"]


def test_validate_invalid():
    datapackage_location = "tests/data/datapackage.json"
    resource_location = "tests/data/invalid/variables.csv"
    result = validator.validate(datapackage_location, resource_location)
    assert not result["valid"]


def test_validate_invalid_resource_name():
    datapackage_location = "tests/data/datapackage.json"
    resource_location = "tests/data/invalid/invalid.csv"
    result = validator.validate(datapackage_location, resource_location)
    assert not result["valid"]
    assert "unknown" in result["message"]
