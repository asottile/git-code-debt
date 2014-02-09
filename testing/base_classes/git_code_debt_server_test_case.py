
import mock
import testify as T

import git_code_debt_server.app
from git_code_debt.generate import main
from testing.base_classes.flask_test_case import FlaskTestCase
from testing.base_classes.sandbox_test_case import SandboxTestCase

@T.suite('integration')
class GitCodeDebtServerTestCase(FlaskTestCase):
    __test__ = False

    FLASK_APPLICATION = git_code_debt_server.app.app


class GitCodeDebtServerWithDataTestCase(GitCodeDebtServerTestCase, SandboxTestCase):
    source_repo = '.'

    @T.setup
    def populate_repo_data(self):
        main([self.source_repo, self.db_path])

    @T.setup_teardown
    def patch_app_db_path(self):
        with mock.patch.object(
            git_code_debt_server.app, 'database_path', self.db_path,
        ):
            yield


