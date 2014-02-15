
import time
import testify as T

from git_code_debt_util.decorators import cached_property
from testing.base_classes.test import test

class Foo(object):
    @cached_property
    def foo(self):
        return "Foo" + str(time.time())

@test
def test_cached_property():
    instance = Foo()
    val = instance.foo
    val2 = instance.foo
    T.assert_is(val, val2)


@test
def test_unbound_cached_property():
    # Make sure we don't blow up when accessing the property unbound
    prop = Foo.foo
    T.assert_isinstance(prop, cached_property)
