
import testify as T

import testing.testing_package.package_a
import testing.testing_package.package_b
from git_code_debt_util.discovery import discover
from testing.base_classes.test import test
from testing.testing_package.package_a.foo import Base


@test
def test_discover_classes():
    # Note: package_a basically just contains a module foo with:
    # class Base(object): pass
    ret = discover(
        testing.testing_package.package_a,
        lambda cls: True,
    )
    T.assert_equal(ret, set([Base]))

@test
def test_discover_excludes_imported_classes():
    # Note: package_b has a module bar which
    # imports Base from package_a.foo and has
    # class Base2(Base): pass
    ret = discover(
        testing.testing_package.package_b,
        lambda cls: True,
    )
    T.assert_not_in(Base, ret)
