
import argparse
import collections
import sqlite3
import sys

from git_code_debt.discovery import get_metric_parsers_from_args
from git_code_debt.file_diff_stat import get_file_diff_stats_from_output
from git_code_debt.logic import get_metric_mapping
from git_code_debt.logic import get_metric_values
from git_code_debt.logic import get_previous_sha
from git_code_debt.logic import insert_metric_values
from git_code_debt.parse_diff_stat import get_stats_from_output
from git_code_debt.repo_parser import RepoParser

def get_metrics(diff, metric_parsers):
    def get_all_metrics(file_diff_stats):
        for metric_parser_cls in metric_parsers:
            metric_parser = metric_parser_cls()
            for metric in metric_parser.get_metrics_from_stat(file_diff_stats):
                yield metric

    file_diff_stats = get_file_diff_stats_from_output(diff)
    return list(get_all_metrics(file_diff_stats))

def increment_metric_values(metric_values, metrics):
    for metric in metrics:
        metric_values[metric.name] += metric.value

def load_data(database_file, repo, package_names, skip_defaults, tempdir_location, debug):
    metric_parsers = get_metric_parsers_from_args(package_names, skip_defaults)

    with sqlite3.connect(database_file) as db:
        metric_mapping = get_metric_mapping(db)

        repo_parser = RepoParser(repo, tempdir_location=tempdir_location)

        with repo_parser.repo_checked_out():
            previous_sha = get_previous_sha(db, repo)
            commits = repo_parser.get_commit_shas(since_sha=previous_sha)

            # If there is nothing to check gtfo
            if len(commits) == 1:
                return

            # Maps metric_name to a running value
            metric_values = collections.defaultdict(int)
            running_total_loc = 0

            # Grab the state of our metrics at the last place
            compare_commit = None
            if previous_sha is not None:
                compare_commit = commits[0]
                metric_values.update(get_metric_values(db, compare_commit))
                commits = commits[1:]

            for commit in commits:
                if compare_commit is None:
                    diff = repo_parser.get_original_commit(commit.sha)
                else:
                    diff = repo_parser.get_commit_diff(compare_commit.sha, commit.sha)

                metrics = get_metrics(diff, metric_parsers)
                increment_metric_values(metric_values, metrics)
                insert_metric_values(db, metric_values, metric_mapping, repo, commit)

                # TODO: debug fails on repositories that have a binary file => symlink change
                if debug:
                    if compare_commit is None:
                        stat_out = repo_parser.get_original_diff_stat(commit.sha)
                    else:
                        stat_out = repo_parser.get_commit_diff_stat(compare_commit.sha, commit.sha)

                    running_total_loc += get_stats_from_output(stat_out)

                    if running_total_loc != metric_values['TotalLinesOfCode']:
                        raise AssertionError(
                            'Integrity of commits compromised.\n'
                            'Diff stat LOC: {0}\n'
                            'Diffs LOC: {1}\n'
                            'Previous SHA: {2}\n'
                            'Current SHA: {3}\n'.format(
                                running_total_loc,
                                metric_values['TotalLinesOfCode'],
                                compare_commit.sha,
                                commit.sha,
                            ),
                        )

                compare_commit = commit

def main(argv):
    parser = argparse.ArgumentParser(description='Generates metrics from a git repo')
    parser.add_argument('repo', help='Repository link to generate metrics from')
    parser.add_argument('database', help='Database file')
    parser.add_argument(
        '--skip-default-metrics',
        default=False,
        action='store_true',
        help='Whether to skip the default metrics',
    )
    parser.add_argument(
        'metric_package_names',
        type=str,
        nargs='*',
        help='Metric Package Names (such as foo.metrics bar.metrics)',
    )
    parser.add_argument(
        '--tempdir-location',
        type=str,
        default=None,
        help='Override location of temp dirs, default is system default.',
    )
    parser.add_argument(
        '--debug',
        default=False,
        action='store_true',
        help='Whether to check diff stats at each iteration',
    )
    args = parser.parse_args(argv)

    load_data(
        args.database,
        args.repo,
        args.metric_package_names,
        args.skip_default_metrics,
        args.tempdir_location,
        args.debug,
    )

if __name__ == '__main__':
    main(sys.argv[1:])
