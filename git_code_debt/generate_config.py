import re
from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Pattern

import cfgv


DEFAULT_GENERATE_CONFIG_FILENAME = 'generate_config.yaml'
SCHEMA = cfgv.Map(
    'Config', 'repo',

    cfgv.Required('repo', cfgv.check_string),
    cfgv.Required('database', cfgv.check_string),
    cfgv.Optional('skip_default_metrics', cfgv.check_bool, False),
    cfgv.Optional(
        'metric_package_names', cfgv.check_array(cfgv.check_string), [],
    ),
    cfgv.Optional('exclude', cfgv.check_regex, '^$'),
)


class GenerateOptions(NamedTuple):
    skip_default_metrics: bool
    metric_package_names: List[str]
    repo: str
    database: str
    exclude: Pattern[bytes]

    @classmethod
    def from_yaml(cls, dct: Dict[str, Any]) -> 'GenerateOptions':
        dct = cfgv.apply_defaults(cfgv.validate(dct, SCHEMA), SCHEMA)
        return cls(
            skip_default_metrics=dct['skip_default_metrics'],
            metric_package_names=dct['metric_package_names'],
            repo=dct['repo'],
            database=dct['database'],
            exclude=re.compile(dct['exclude'].encode()),
        )
