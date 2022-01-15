from __future__ import annotations

import re

import cfgv
import pytest

from git_code_debt.generate_config import GenerateOptions


def test_empty_config_invalid():
    with pytest.raises(cfgv.ValidationError):
        GenerateOptions.from_yaml({})


def test_with_all_options_specified():
    ret = GenerateOptions.from_yaml({
        'skip_default_metrics': True,
        'metric_package_names': ['my_package'],
        'repo': '.',
        'database': 'database.db',
        'exclude': '^vendor/',
    })
    assert ret == GenerateOptions(
        skip_default_metrics=True,
        metric_package_names=['my_package'],
        repo='.',
        database='database.db',
        exclude=re.compile(b'^vendor/'),
    )


def test_minimal_defaults():
    ret = GenerateOptions.from_yaml({'repo': './', 'database': 'database.db'})
    assert ret == GenerateOptions(
        skip_default_metrics=False,
        metric_package_names=[],
        repo='./',
        database='database.db',
        exclude=re.compile(b'^$'),
    )
