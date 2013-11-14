
import mock
import testify as T

import git_code_debt.config

class TestLoadConfig(T.TestCase):

    def test_load_config(self):
        with mock.patch.object(
            git_code_debt.config,
            'CONFIG_FILE',
            'example_config.yaml',
        ):
            config_contents = git_code_debt.config.load_config()

        T.assert_equal(
            config_contents,
            {
                'git-repo-url': 'git@github.com:asottile/git-code-debt',
                'git-repo-ref': 'master',
            }
        )
