from __future__ import absolute_import
from __future__ import unicode_literals

import jsonschema.exceptions
import pytest

from git_code_debt.generate_config import GenerateOptions


def test_empty_config_invalid():
    with pytest.raises(jsonschema.exceptions.ValidationError):
        GenerateOptions.from_yaml({})


def test_with_all_options_specified():
    ret = GenerateOptions.from_yaml({
        'skip_default_metrics': True,
        'metric_package_names': ['my_package'],
        'repo': '.',
        'database': 'database.db',
    })
    assert ret == GenerateOptions(
        skip_default_metrics=True,
        metric_package_names=['my_package'],
        repo='.',
        database='database.db',
    )


def test_minimal_defaults():
    ret = GenerateOptions.from_yaml({'repo': './', 'database': 'database.db'})
    assert ret == GenerateOptions(
        skip_default_metrics=False,
        metric_package_names=[],
        repo='./',
        database='database.db',
    )


def test_none_for_tempdir_allowed():
    ret = GenerateOptions.from_yaml({
        'repo': 'repo',
        'database': 'database.db',
    })
    assert ret == GenerateOptions(
        skip_default_metrics=False,
        metric_package_names=[],
        repo='repo',
        database='database.db',
    )


def test_to_yaml_all_specified():
    ret = GenerateOptions(
        skip_default_metrics=True,
        metric_package_names=['my_package'],
        repo='.',
        database='database.db',
    ).to_yaml()

    assert ret == {
        'skip_default_metrics': True,
        'metric_package_names': ['my_package'],
        'repo': '.',
        'database': 'database.db',
    }


def test_to_yaml_defaults():
    ret = GenerateOptions(
        skip_default_metrics=False,
        metric_package_names=[],
        repo='.',
        database='database.db',
    ).to_yaml()
    assert ret == {'repo': '.', 'database': 'database.db'}
