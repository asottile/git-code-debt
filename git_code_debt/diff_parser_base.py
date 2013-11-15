
import collections

class Status(object):
    ADDED = object()
    DELETED = object()
    ALREADY_EXISTING = object()

FileDiffStat = collections.namedtuple(
    'FileStat',
    ['filename', 'lines_added', 'lines_removed', 'status'],
)

def _to_file_diff_stat(filename_from, filename_to, lines_added, lines_removed):
    if filename_from == 'dev/null':
        status = Status.ADDED
        filename = filename_to
    elif filename_to == 'dev/null':
        status = Status.DELETED
        filename = filename_from
    else:
        assert filename_from == filename_to, u'{0} => {1}'.format(filename_from, filename_to)
        status = Status.ALREADY_EXISTING
        filename = filename_to

    return FileDiffStat(filename, lines_added, lines_removed, status)

def _get_file_diff_stats_from_output_helper(output):
    filename_from = None
    filename_to = None
    lines_added = None
    lines_removed = None

    NEWLINE = '\n'
    lines_iter = iter(output.split(NEWLINE))

    try:
        while True:
            line = lines_iter.next()
            if line.startswith('diff --git'):
                if filename_from is not None and filename_to is not None:
                    yield _to_file_diff_stat(
                        filename_from,
                        filename_to,
                        lines_added,
                        lines_removed,
                    )

                    filename_from = None
                    filename_to = None
                    lines_added = None
                    lines_removed = None

                # exhaust the index line
                lines_iter.next()
                from_line = lines_iter.next()
                # Scan until the from file line
                while not from_line.startswith('--- '):
                    from_line = lines_iter.next()

                assert from_line.startswith('--- ')

                # To line is directly after it
                to_line = lines_iter.next()
                assert to_line.startswith('+++ ')
                filename_from = from_line[4:].lstrip('a').lstrip('/')
                filename_to = to_line[4:].lstrip('b').lstrip('/')
                lines_added = []
                lines_removed = []

            # If we're in the context of a file
            elif filename_from is not None and filename_to is not None:
                if line.startswith('+'):
                    lines_added.append(line[1:])
                elif line.startswith('-'):
                    lines_removed.append(line[1:])

    except StopIteration:
        # At the very end we want to yield the last FileDiffStat
        if filename_from is not None and filename_to is not None:
            yield _to_file_diff_stat(
                filename_from,
                filename_to,
                lines_added,
                lines_removed,
            )

def get_file_diff_stats_from_output(output):
    return list(_get_file_diff_stats_from_output_helper(output))

class DiffParserBase(object):
    """Generates metrics from git show"""

    def get_metrics_from_stat(self, file_diff_stats):
        """Implement me to yield Metric objects from the input list of
        FileStat objects.

        Args:
            file_diff_stats - list of FileDiffStat objects

        Returns:
           generator of Metric objects
        """
        raise NotImplementedError

    def get_possible_metric_ids(self):
        raise NotImplementedError
