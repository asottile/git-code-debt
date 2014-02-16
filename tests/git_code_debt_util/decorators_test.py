
import time

from git_code_debt_util.decorators import cached_property


class Foo(object):
    @cached_property
    def foo(self):
        return "Foo" + str(time.time())


def test_cached_property():
    instance = Foo()
    val = instance.foo
    val2 = instance.foo
    assert val is val2


def test_unbound_cached_property():
    # Make sure we don't blow up when accessing the property unbound
    prop = Foo.foo
    assert isinstance(prop, cached_property)
