
import time
import testify as T

from git_code_debt_util.decorators import cached_property

class TestCachedProperty(T.TestCase):

    class Foo(object):
        @cached_property
        def foo(self):
            return "Foo" + str(time.time())

    def test_cached_property(self):
        instance = self.Foo()
        val = instance.foo
        val2 = instance.foo
        T.assert_is(val, val2)


    def test_unbound_cached_property(self):
        # Make sure we don't blow up when accessing the property unbound
        prop = self.Foo.foo
        T.assert_isinstance(prop, cached_property)

if __name__ == '__main__':
    T.run()
