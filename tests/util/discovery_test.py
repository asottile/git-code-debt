
import testify as T

from util.discovery import get_module_name

class TestGetModuleName(T.TestCase):
    """Tests the get_module_name function."""

    def test_get_module_name(self):
        module_name = get_module_name('foo', 'bar.py')
        T.assert_equal(module_name, 'foo.bar')

    def test_raises_on_non_python_file(self):
        with T.assert_raises(ValueError):
            get_module_name('foo', 'bar')

    def test_more_complicated_directory(self):
        module_name = get_module_name('foo/bar', 'baz.py')
        T.assert_equal(module_name, 'foo.bar.baz')

    def test_strips_prefixing_dot_slash(self):
        module_name = get_module_name('./foo', 'bar.py')
        T.assert_equal(module_name, 'foo.bar')
