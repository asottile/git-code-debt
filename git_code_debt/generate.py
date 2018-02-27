from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import collections
import io
import itertools
import multiprocessing.pool
import os
import os.path
import sqlite3

import pkg_resources
import six
import yaml

from git_code_debt import options
from git_code_debt.discovery import get_metric_parsers_from_args
from git_code_debt.file_diff_stat import get_file_diff_stats_from_output
from git_code_debt.generate_config import GenerateOptions
from git_code_debt.logic import get_metric_has_data
from git_code_debt.logic import get_metric_mapping
from git_code_debt.logic import get_metric_values
from git_code_debt.logic import get_previous_sha
from git_code_debt.repo_parser import RepoParser
from git_code_debt.write_logic import insert_metric_changes
from git_code_debt.write_logic import insert_metric_values


def get_metrics(commit, diff, metric_parsers, exclude):
    def get_all_metrics(file_diff_stats):
        for metric_parser_cls in metric_parsers:
            metric_parser = metric_parser_cls()
            for metric in metric_parser.get_metrics_from_stat(
                commit, file_diff_stats,
            ):
                yield metric

    file_diff_stats = get_file_diff_stats_from_output(diff)
    file_diff_stats = tuple(
        x for x in file_diff_stats
        if not exclude.search(x.path)
    )
    return tuple(get_all_metrics(file_diff_stats))


def increment_metric_values(metric_values, metric_mapping, metrics):
    metric_values.update({metric_mapping[m.name]: m.value for m in metrics})


def _get_metrics_inner(mp_args):
    compare_commit, commit, repo_parser, metric_parsers, exclude = mp_args
    if compare_commit is None:
        diff = repo_parser.get_original_commit(commit.sha)
    else:
        diff = repo_parser.get_commit_diff(compare_commit.sha, commit.sha)
    return get_metrics(commit, diff, metric_parsers, exclude)


def mapper(jobs):
    if jobs == 1:
        return map
    else:
        return multiprocessing.Pool(jobs).imap


def update_has_data(db, metrics, metric_mapping, has_data):
    query = 'UPDATE metric_names SET has_data=1 WHERE id = ?'
    for metric_id in [metric_mapping[m.name] for m in metrics if m.value]:
        if not has_data[metric_id]:
            has_data[metric_id] = True
            db.execute(query, (metric_id,))


def load_data(
        database_file,
        repo,
        package_names,
        skip_defaults,
        exclude,
        jobs,
):
    metric_parsers = get_metric_parsers_from_args(package_names, skip_defaults)

    with sqlite3.connect(database_file) as db:
        metric_mapping = get_metric_mapping(db)  # type: Dict[str, int]
        has_data = get_metric_has_data(db)  # type: Dict[int, bool]

        repo_parser = RepoParser(repo)

        with repo_parser.repo_checked_out():
            previous_sha = get_previous_sha(db)
            commits = repo_parser.get_commits(since_sha=previous_sha)

            # If there is nothing to check gtfo
            if len(commits) == 1 and previous_sha is not None:
                return

            # Maps metric_id to a running value
            metric_values = collections.Counter()  # type: Counter[int]

            # Grab the state of our metrics at the last place
            compare_commit = None
            if previous_sha is not None:
                compare_commit = commits.pop(0)
                metric_values.update(get_metric_values(db, compare_commit.sha))

            mp_args = six.moves.zip(
                [compare_commit] + commits,
                commits,
                itertools.repeat(repo_parser),
                itertools.repeat(metric_parsers),
                itertools.repeat(exclude),
            )
            do_map = mapper(jobs)
            for commit, metrics in six.moves.zip(
                    commits, do_map(_get_metrics_inner, mp_args),
            ):
                update_has_data(db, metrics, metric_mapping, has_data)
                increment_metric_values(metric_values, metric_mapping, metrics)
                insert_metric_values(db, metric_values, has_data, commit)
                insert_metric_changes(db, metrics, metric_mapping, commit)


def create_schema(db):
    """Creates the database schema."""
    schema_dir = pkg_resources.resource_filename('git_code_debt', 'schema')
    schema_files = os.listdir(schema_dir)

    for sql_file in schema_files:
        resource_filename = os.path.join(schema_dir, sql_file)
        with open(resource_filename, 'r') as resource:
            db.executescript(resource.read())


def get_metrics_info(metric_parsers):
    metrics_info = set()
    for metric_parser_cls in metric_parsers:
        metrics_info.update(metric_parser_cls().get_metrics_info())
    return sorted(metrics_info)


def insert_metrics_info(db, metrics_info):
    query = 'INSERT INTO metric_names (name, description) VALUES (?, ?)'
    db.executemany(query, metrics_info)


def populate_metric_ids(db, package_names, skip_defaults):
    metric_parsers = get_metric_parsers_from_args(package_names, skip_defaults)
    metrics_info = get_metrics_info(metric_parsers)
    insert_metrics_info(db, metrics_info)


def create_database(args):
    with sqlite3.connect(args.database) as db:
        create_schema(db)
        populate_metric_ids(
            db,
            args.metric_package_names,
            args.skip_default_metrics,
        )


def get_options_from_config(config_filename):
    if not os.path.exists(config_filename):
        print('config file not found {}'.format(config_filename))
        exit(1)

    with io.open(config_filename) as config_file:
        return GenerateOptions.from_yaml(yaml.load(config_file))


def main(argv=None):
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


if __name__ == '__main__':
    exit(main())
