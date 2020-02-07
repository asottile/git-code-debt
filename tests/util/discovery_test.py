import testing.testing_package.package_a
import testing.testing_package.package_b
from git_code_debt.util.discovery import discover
from testing.testing_package.package_a.base import Base


def test_discover_classes():
    # Note: package_a basically just contains a module base with:
    # class Base(object): pass
    ret = discover(
        testing.testing_package.package_a,
        lambda cls: True,
    )
    assert ret == {Base}


def test_discover_excludes_imported_classes():
    # Note: package_b has a module derived which
    # imports Base from package_a.base and has
    # class Base2(Base): pass
    ret = discover(
        testing.testing_package.package_b,
        lambda cls: True,
    )
    assert Base not in ret
