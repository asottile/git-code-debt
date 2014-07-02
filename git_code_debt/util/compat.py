from __future__ import absolute_import
from __future__ import unicode_literals

from git_code_debt.util import five


# pylint:disable=import-error,no-name-in-module,unused-import


if five.PY2:  # pragma: no cover (PY2 only)
    import __builtin__ as builtins  # noqa
    import urlparse as urllib_parse  # noqa
else:  # pragma: no cover (PY3 only)
    import builtins  # noqa
    import urllib.parse as urllib_parse  # noqa
