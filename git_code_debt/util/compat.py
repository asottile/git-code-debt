from __future__ import absolute_import
from __future__ import unicode_literals

import six


if six.PY2:  # pragma: no cover (PY2 only)
    import __builtin__ as builtins  # noqa
    import urlparse as urllib_parse  # noqa
else:  # pragma: no cover (PY3 only)
    import builtins  # noqa
    import urllib.parse as urllib_parse  # noqa
