# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,redefined-outer-name
"""Test cases for builder.py"""

import pytest

from ddionrails_datapackage import builder

INVALID_CONFIGS = [{}, {"metadata": {}}, {"files": []}]


@pytest.mark.parametrize("invalid_config", INVALID_CONFIGS)
def test_build_fails(invalid_config):
    """Test that fails with invalid config dictionary."""
    with pytest.raises(ValueError):
        builder.build(invalid_config)


@pytest.fixture
def config():
    return {"metadata": {"name": "ddionrails-study"}, "files": ["variables.csv"]}


def test_build(config):
    package = builder.build(config)
    assert package.descriptor["name"] == config["metadata"]["name"]
    assert "foreignKeys" not in package.descriptor["resources"][0]["schema"]


@pytest.fixture
def config_strict():
    return {"metadata": {"name": "ddionrails-study"}, "files": ["variables_strict.csv"]}


def test_build_strict(config_strict):
    """Tests that _strict rules are loaded and foreignKeys are part of the schema."""
    package = builder.build(config_strict)
    assert "foreignKeys" in package.descriptor["resources"][0]["schema"]


def test_build_invalid(config, caplog):
    config["files"] = []
    package = builder.build(config)
    assert not package.valid
    for record in caplog.records:
        assert "Descriptor validation error" in str(record.msg)
