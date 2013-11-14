
import os.path
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))

CONFIG_FILE = 'config.yaml'

def load_config():
    yaml_filename = os.path.join(ROOT, CONFIG_FILE)
    if not os.path.exists(yaml_filename):
        raise AssertionError(
            'config.yaml does not exist.  Expected at {0}'.format(
               yaml_filename
            )
        )

    with open(yaml_filename, 'r') as yaml_file:
        return yaml.load(yaml_file)
