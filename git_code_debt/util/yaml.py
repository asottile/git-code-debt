import functools

import yaml


Loader = getattr(yaml, 'CSafeLoader', yaml.SafeLoader)
load = functools.partial(yaml.load, Loader=Loader)
Dumper = getattr(yaml, 'CSafeDumper', yaml.SafeDumper)
dump = functools.partial(yaml.dump, Dumper=Dumper)
