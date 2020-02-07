from typing import NamedTuple


SIGNS_TO_CLASSNAMES = {
    0: 'metric-none',
    1: 'metric-up',
    -1: 'metric-down',
}


class Delta(NamedTuple):
    url: str
    value: int

    @property
    def classname(self) -> str:
        if not self.value:
            sign = 0
        else:
            sign = self.value // abs(self.value)

        return SIGNS_TO_CLASSNAMES[sign]
