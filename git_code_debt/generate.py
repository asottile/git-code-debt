
import argparse
import collections
import re

from git_code_debt.diff_parser_base import get_file_diff_stats_from_output
from git_code_debt.discovery import get_metric_parsers
from git_code_debt.repo_parser import RepoParser
from git_code_debt_server.app import get_database

STAT_INSERTIONS_RE = re.compile('(\d+) insertion')
STAT_DELETIONS_RE = re.compile('(\d+) deletion')

def get_stats_from_output(stat_out):
    stat_line = stat_out.splitlines()[-1]
    insertions = STAT_INSERTIONS_RE.search(stat_line)
    deletions = STAT_DELETIONS_RE.search(stat_line)

    return (
        (int(insertions.group(1)) if insertions else 0) -
        (int(deletions.group(1)) if deletions else 0)
    )

def get_metric_outputs(diff):
    def get_all_metrics(file_diff_stats):
        for metric_parser_cls in get_metric_parsers():
            metric_parser = metric_parser_cls()
            for metric in metric_parser.get_metrics_from_stat(file_diff_stats):
                yield metric

    file_diff_stats = get_file_diff_stats_from_output(diff)
    return list(get_all_metrics(file_diff_stats))

def increment_metric_values(metric_values, metrics):
    for metric in metrics:
        metric_values[metric.metric_name] += metric.value

def get_metric_mapping(database):
    results = database.execute("""
        SELECT
            name,
            id
        FROM metric_names
    """).fetchall()
    return dict(results)

def get_previous_sha(database, repo):
    result = database.execute(
        """
        SELECT
            sha
        FROM metric_data
        WHERE repo = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        [repo]
    ).fetchone()

    return result[0] if result else None

def get_metric_values(database, commit):
    results = database.execute(
        '''
        SELECT
            metric_names.name,
            running_value
        FROM metric_data
        INNER JOIN metric_names ON
            metric_names.id = metric_data.metric_id
        WHERE sha = ?
        ''',
        [commit.sha],
    )
    return dict(results)

def insert_metric_values(database, metric_values, metric_mapping, repo, commit):
    for metric_name, value in metric_values.iteritems():
        metric_id = metric_mapping[metric_name]
        database.execute(
            '''
            INSERT INTO metric_data
            (repo, sha, metric_id, timestamp, running_value)
            VALUES (?, ?, ?, ?, ?)
            ''',
            [repo, commit.sha, metric_id, commit.date, value],
        )

def load_data(repo):
    with get_database() as database:
        repo_parser = RepoParser(repo)

        with repo_parser.repo_checked_out():
            previous_sha = get_previous_sha(database, repo)

            metric_mapping = get_metric_mapping(database)

            commits = repo_parser.get_commit_shas(since_sha=previous_sha)

            # If there is nothing to check gtfo
            if not commits:
                return

            # Maps metric_name to a running value
            metric_values = collections.defaultdict(int)
            running_total_loc = 0

            # Grab the state of our metrics at the last place
            compare_commit = None
            if previous_sha is not None:
                compare_commit = commits[0]
                metric_values.update(get_metric_values(database, compare_commit))
                commits = commits[1:]

            for commit in commits:
                if compare_commit is None:
                    diff = repo_parser.get_original_commit(commit.sha)
                    stat_out = repo_parser.get_original_diff_stat(commit.sha)
                else:
                    diff = repo_parser.get_commit_diff(compare_commit.sha, commit.sha)
                    stat_out = repo_parser.get_commit_diff_stat(compare_commit.sha, commit.sha)

                metrics = get_metric_outputs(diff)
                increment_metric_values(metric_values, metrics)
                insert_metric_values(database, metric_values, metric_mapping, repo, commit)

                running_total_loc +=  get_stats_from_output(stat_out)
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

def main():
    parser = argparse.ArgumentParser(description='Generates metrics from a git repo')
    parser.add_argument('repo', help='Repository link to generate metrics from')
    parser.add_argument('--from-sha', type=str, help='Start repo from date')
    args = parser.parse_args()

    load_data(args.repo)

if __name__ == '__main__':
    main()
