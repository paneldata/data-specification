# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,redefined-outer-name
"""Test cases for cli.py"""

import pytest
from click.testing import CliRunner

from ddionrails_datapackage import cli


@pytest.fixture
def mocked_build(mocker):
    return mocker.patch("ddionrails_datapackage.builder.build")


def test_cli():
    result = CliRunner().invoke(cli.cli)
    assert result.exit_code == 0
    assert "ddionrails datapackage CLI" in result.output


def test_cli_build_without_config():
    result = CliRunner().invoke(cli.cli, ["build"])
    assert result.exit_code == 2
    assert "does not exist." in result.output


def test_cli_build_with_config(tmp_path):
    path = tmp_path.joinpath("datapackage.json")
    result = CliRunner().invoke(
        cli.cli, ["build", "tests/data/example-config.yml", str(path)]
    )
    assert result.exit_code == 0
    assert result.output == ""


def test_infer_path(tmp_path):
    path = tmp_path.joinpath("datapackage.json")
    result = CliRunner().invoke(
        cli.cli, ["infer", "tests/data/valid-resource", str(path)]
    )
    assert result.exit_code == 0
    assert result.output == ""


def test_infer_strict(tmp_path):
    path = tmp_path.joinpath("datapackage.json")
    result = CliRunner().invoke(
        cli.cli, ["infer", "tests/data/valid-resource", str(path), "--strict"]
    )
    assert result.exit_code == 0
    assert result.output == ""


def test_cli_validate_without_argument():
    result = CliRunner().invoke(cli.cli, ["validate"])
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_cli_validate_with_argument_and_missing_file():
    result = CliRunner().invoke(
        cli.cli,
        ["validate", "tests/data/valid-resource/datapackage.json", "missing-resource"],
    )
    assert result.exit_code == 1
    assert '"valid": false' in result.output


def test_cli_validate_with_argument_existing_file():
    result = CliRunner().invoke(
        cli.cli, ["validate", "tests/data/valid-resource/datapackage.json", "variables"]
    )
    assert result.exit_code == 0
    assert '"valid": true' in result.output


def test_cli_validate_with_valid_check_relations():
    """Tests that validate --check-relations follows foreign keys."""
    result = CliRunner().invoke(
        cli.cli,
        [
            "validate",
            "tests/data/valid-relations/datapackage.json",
            "--check-relations",
        ],
    )
    assert result.exit_code == 0
    assert '"valid": true' in result.output


def test_cli_validate_with_invalid_check_relations():
    """Tests that validate --check-relations follows foreign keys and fails."""
    result = CliRunner().invoke(
        cli.cli,
        [
            "validate",
            "tests/data/invalid-relations/datapackage.json",
            "--check-relations",
        ],
    )
    assert result.exit_code == 0
    assert '"valid": true' in result.output
    assert "Foreign key" in result.output
