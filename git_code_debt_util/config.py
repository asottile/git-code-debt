
import functools

import staticconf


def get_config_watcher(filename, namespace):
    loader = functools.partial(staticconf.YamlConfiguration, filename, namespace=namespace)
    reloader = staticconf.config.ReloadCallbackChain(namespace=namespace)
    watcher = staticconf.ConfigurationWatcher(
        loader,
        filename,
        min_interval=10,
        reloader=reloader,
    )
    # Initial load
    watcher.config_loader()
    return watcher
