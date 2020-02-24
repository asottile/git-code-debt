import argparse
import collections
import contextlib
import itertools
import multiprocessing.pool
import os.path
import sqlite3
from typing import Callable
from typing import Counter
from typing import Dict
from typing import Generator
from typing import Iterable
from typing import List
from typing import Optional
from typing import Pattern
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar

import pkg_resources

from git_code_debt import options
from git_code_debt.discovery import get_metric_parsers_from_args
from git_code_debt.file_diff_stat import FileDiffStat
from git_code_debt.file_diff_stat import get_file_diff_stats_from_output
from git_code_debt.generate_config import GenerateOptions
from git_code_debt.logic import get_metric_has_data
from git_code_debt.logic import get_metric_mapping
from git_code_debt.logic import get_metric_values
from git_code_debt.logic import get_previous_sha
from git_code_debt.metric import Metric
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt.metrics.base import MetricInfo
from git_code_debt.repo_parser import Commit
from git_code_debt.repo_parser import RepoParser
from git_code_debt.util import yaml
from git_code_debt.write_logic import insert_metric_changes
from git_code_debt.write_logic import insert_metric_values


def get_metrics(
        commit: Commit,
        diff: bytes, metric_parsers:
        Set[Type[DiffParserBase]],
        exclude: Pattern[bytes],
) -> Tuple[Metric, ...]:
    def get_all_metrics(
            file_diff_stats: Tuple[FileDiffStat, ...],
    ) -> Generator[Metric, None, None]:
        for metric_parser_cls in metric_parsers:
            metric_parser = metric_parser_cls()
            yield from metric_parser.get_metrics_from_stat(
                commit, file_diff_stats,
            )

    file_diff_stats = tuple(
        x for x in get_file_diff_stats_from_output(diff)
        if not exclude.search(x.path)
    )
    return tuple(get_all_metrics(file_diff_stats))


def increment_metrics(
        metric_values: Counter[int],
        metric_mapping: Dict[str, int],
        metrics: Tuple[Metric, ...],
) -> None:
    metric_values.update({metric_mapping[m.name]: m.value for m in metrics})


def _get_metrics_inner(
        mp_args: Tuple[
            Optional[Commit],
            Commit,
            RepoParser,
            Set[Type[DiffParserBase]],
            Pattern[bytes],
        ],
) -> Tuple[Metric, ...]:
    compare_commit, commit, repo_parser, metric_parsers, exclude = mp_args
    if compare_commit is None:
        diff = repo_parser.get_original_commit(commit.sha)
    else:
        diff = repo_parser.get_commit_diff(compare_commit.sha, commit.sha)
    return get_metrics(commit, diff, metric_parsers, exclude)


T = TypeVar('T')
T2 = TypeVar('T2')


@contextlib.contextmanager
def mapper(jobs: int) -> Generator[
    Callable[[Callable[[T2], T], Iterable[T2]], Iterable[T]], None, None,
]:
    if jobs == 1:
        yield map
    else:
        with contextlib.closing(multiprocessing.Pool(jobs)) as pool:
            yield pool.imap


def update_has_data(
        db: sqlite3.Connection,
        metrics: Tuple[Metric, ...],
        metric_mapping: Dict[str, int],
        has_data: Dict[int, bool],
) -> None:
    query = 'UPDATE metric_names SET has_data=1 WHERE id = ?'
    for metric_id in [metric_mapping[m.name] for m in metrics if m.value]:
        if not has_data[metric_id]:
            has_data[metric_id] = True
            db.execute(query, (metric_id,))


def load_data(
        database_file: str,
        repo: str,
        package_names: List[str],
        skip_defaults: bool,
        exclude: Pattern[bytes],
        jobs: int,
) -> None:
    metric_parsers = get_metric_parsers_from_args(package_names, skip_defaults)

    with sqlite3.connect(database_file) as db:
        metric_mapping = get_metric_mapping(db)
        has_data = get_metric_has_data(db)

        repo_parser = RepoParser(repo)

        with repo_parser.repo_checked_out():
            previous_sha = get_previous_sha(db)
            commits = repo_parser.get_commits(since_sha=previous_sha)

            # If there is nothing to check gtfo
            if len(commits) == 1 and previous_sha is not None:
                return

            # Maps metric_id to a running value
            metric_values: Counter[int] = collections.Counter()

            # Grab the state of our metrics at the last place
            compare_commit = None
            if previous_sha is not None:
                compare_commit = commits.pop(0)
                metric_values.update(get_metric_values(db, compare_commit.sha))

            mp_args = zip(
                [compare_commit, *commits],
                commits,
                itertools.repeat(repo_parser),
                itertools.repeat(metric_parsers),
                itertools.repeat(exclude),
            )
            with mapper(jobs) as do_map:
                for commit, metrics in zip(
                        commits, do_map(_get_metrics_inner, mp_args),
                ):
                    update_has_data(db, metrics, metric_mapping, has_data)
                    increment_metrics(metric_values, metric_mapping, metrics)
                    insert_metric_values(db, metric_values, has_data, commit)
                    insert_metric_changes(db, metrics, metric_mapping, commit)


def create_schema(db: sqlite3.Connection) -> None:
    """Creates the database schema."""
    schema_dir = pkg_resources.resource_filename('git_code_debt', 'schema')
    schema_files = os.listdir(schema_dir)

    for sql_file in schema_files:
        resource_filename = os.path.join(schema_dir, sql_file)
        with open(resource_filename, 'r') as resource:
            db.executescript(resource.read())


def get_metrics_info(
        metric_parsers: Set[Type[DiffParserBase]],
) -> List[MetricInfo]:
    metrics_info = set()
    for metric_parser_cls in metric_parsers:
        metrics_info.update(metric_parser_cls().get_metrics_info())
    return sorted(metrics_info)


def insert_metrics_info(
        db: sqlite3.Connection,
        metrics_info: List[MetricInfo],
) -> None:
    query = 'INSERT INTO metric_names (name, description) VALUES (?, ?)'
    db.executemany(query, metrics_info)


def populate_metric_ids(
        db: sqlite3.Connection,
        package_names: List[str],
        skip_defaults: bool,
) -> None:
    metric_parsers = get_metric_parsers_from_args(package_names, skip_defaults)
    metrics_info = get_metrics_info(metric_parsers)
    insert_metrics_info(db, metrics_info)


def create_database(args: GenerateOptions) -> None:
    with sqlite3.connect(args.database) as db:
        create_schema(db)
        populate_metric_ids(
            db,
            args.metric_package_names,
            args.skip_default_metrics,
        )


def get_options_from_config(config_filename: str) -> GenerateOptions:
    if not os.path.exists(config_filename):
        print(f'config file not found {config_filename}')
        exit(1)

    with open(config_filename) as config_file:
        return GenerateOptions.from_yaml(yaml.load(config_file))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    options.add_generate_config_filename(parser)
    parser.add_argument(
        '-j', '--jobs', type=int, default=multiprocessing.cpu_count(),
    )
    parsed_args = parser.parse_args(argv)
    args = get_options_from_config(parsed_args.config_filename)

    if not os.path.exists(args.database):
        create_database(args)

    load_data(
        args.database,
        args.repo,
        args.metric_package_names,
        args.skip_default_metrics,
        args.exclude,
        parsed_args.jobs,
    )
    return 0


if __name__ == '__main__':
    exit(main())
