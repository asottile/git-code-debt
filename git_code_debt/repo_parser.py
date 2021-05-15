import abc
import contextlib
from typing import Generator
from typing import List
from typing import NamedTuple
from typing import Optional


class Commit(NamedTuple):
    sha: str
    date: int


BLANK_COMMIT = Commit('0' * 40, 0)


class RepoParser(abc.ABC):

    def __init__(self) -> None:
        self.tempdir: Optional[str] = None

    @contextlib.contextmanager
    @abc.abstractmethod
    def repo_checked_out(self) -> Generator[None, None, None]:
        """ This needs to check out the repository to the temp directory. """

    @abc.abstractmethod
    def get_commit(self, sha: str) -> Commit:
        """Returns a Commit object for.

        Args:
            sha - A sha for the commit
        """

    @abc.abstractmethod
    def get_commits(self, since_sha: Optional[str] = None) -> List[Commit]:
        """Returns a list of Commit objects.

        Args:
           since_sha - (optional) A sha to search from
        """

    @abc.abstractmethod
    def get_original_commit(self, sha: str) -> bytes:
        """Returns the raw output of the commit """

    @abc.abstractmethod
    def get_commit_diff(self, previous_sha: str, sha: str) -> bytes:
        """Returns the raw output of the diff between previous_sha and sha"""


