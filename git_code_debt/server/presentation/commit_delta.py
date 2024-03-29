from __future__ import annotations

from typing import NamedTuple

from git_code_debt.server.presentation.delta import Delta


class CommitDelta(NamedTuple):
    metric_name: str
    classname: str
    delta: Delta

    @classmethod
    def from_data(
            cls,
            metric_name: str,
            delta: Delta,
            color_overrides: set[str],
    ) -> CommitDelta:
        return cls(
            metric_name,
            # TODO: duplicated in Metric
            'color-override' if metric_name in color_overrides else '',
            delta,
        )
