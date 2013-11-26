
import testify as T

from git_code_debt_util.discovery import discover
from testing.testing_package.package_a.foo import Base
import testing.testing_package.package_a
import testing.testing_package.package_b


class TestDiscover(T.TestCase):

    def test_discover_classes(self):
        # Note: package_a basically just contains a module foo with:
        # class Base(object): pass
        ret = discover(
            testing.testing_package.package_a,
            lambda cls: True,
        )
        T.assert_equal(ret, set([Base]))

    def test_discover_excludes_imported_classes(self):
        # Note: package_b has a module bar which
        # imports Base from package_a.foo and has
        # class Base2(Base): pass
        ret = discover(
            testing.testing_package.package_b,
            lambda cls: True,
        )
        T.assert_not_in(Base, ret)
