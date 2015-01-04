from __future__ import absolute_import
from __future__ import unicode_literals

import collections

import jsonschema


DEFAULT_GENERATE_CONFIG_FILENAME = 'generate_config.yaml'


GENERATE_OPTIONS_SCHEMA = {
    'type': 'object',
    'required': ['repo', 'database'],
    'properties': {
        'skip_default_metrics': {'type': 'boolean'},
        'tempdir_location': {'type': ['string', 'null']},
        'metric_package_names': {'type': 'array', 'items': {'type': 'string'}},
        'repo': {'type': 'string'},
        'database': {'type': 'string'},
    },
}


class GenerateOptions(collections.namedtuple(
        'GenerateOptions',
        [
            'skip_default_metrics',
            'tempdir_location',
            'metric_package_names',
            'repo',
            'database',
        ],
)):
    @classmethod
    def from_yaml(cls, yaml_dict):
        jsonschema.validate(yaml_dict, GENERATE_OPTIONS_SCHEMA)
        return cls(
            skip_default_metrics=yaml_dict.get('skip_default_metrics', False),
            tempdir_location=yaml_dict.get('tempdir_location', None),
            metric_package_names=yaml_dict.get('metric_package_names', []),
            repo=yaml_dict['repo'],
            database=yaml_dict['database'],
        )

    def to_yaml(self):
        ret = {'repo': self.repo, 'database': self.database}
        if self.skip_default_metrics is True:
            ret['skip_default_metrics'] = True
        if self.metric_package_names:
            ret['metric_package_names'] = list(self.metric_package_names)
        if self.tempdir_location:
            ret['tempdir_location'] = self.tempdir_location

        return ret
