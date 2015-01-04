from __future__ import absolute_import
from __future__ import unicode_literals

import functools

import staticconf

from git_code_debt.server.metric_config import CONFIG_NAMESPACE


watcher = staticconf.ConfigFacade.load(
    'metric_config.yaml',
    CONFIG_NAMESPACE,
    functools.partial(staticconf.YamlConfiguration, flatten=False),
    min_interval=30,
)
