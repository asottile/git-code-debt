from __future__ import absolute_import
from __future__ import unicode_literals


# pylint:disable=invalid-name,undefined-variable
PY2 = str is bytes
PY3 = str is not bytes

if PY2:  # pragma: no cover (PY2 only)
    text = unicode  # flake8: noqa
else:  # pragma: no cover (PY3 only)
    text = str
