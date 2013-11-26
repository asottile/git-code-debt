
import re

STAT_INSERTIONS_RE = re.compile('(\d+) insertion')
STAT_DELETIONS_RE = re.compile('(\d+) deletion')

def get_stats_from_output(stat_out):
    # Sometimes there are empty diffs
    if not stat_out:
        return 0

    stat_line = stat_out.splitlines()[-1]
    insertions = STAT_INSERTIONS_RE.search(stat_line)
    deletions = STAT_DELETIONS_RE.search(stat_line)

    return (
        (int(insertions.group(1)) if insertions else 0) -
        (int(deletions.group(1)) if deletions else 0)
    )
