[![Build Status](https://asottile.visualstudio.com/asottile/_apis/build/status/asottile.git-code-debt?branchName=master)](https://asottile.visualstudio.com/asottile/_build/latest?definitionId=16&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/16/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=16&branchName=master)

git-code-debt
=============

A dashboard for monitoring code debt in a git repository.


## Installation

`pip install git-code-debt`


## Usage


### Basic / tl;dr Usage

#### make a `generate_config.yaml`

```yaml
# required: repository to clone (can be anything `git clone` understands) even
# a repository already on disk
repo: git@github.com:asottile/git-code-debt

# required: database generation path
database: database.db

# optional: default False
skip_default_metrics: false

# optional: default []
metric_package_names: []

# optional: default ^$ (python regex) to exclude paths such as '^vendor/'
exclude: ^$
```

#### invoke the cli

```
# Generate code metric data (substitute your own repo path)
$ git-code-debt-generate
# Start the server
$ git-code-debt-server database.db
```

### Updating data on an existing database

Adding data to the database is as simple as running generate again.
`git-code-debt` will pick up in the git history from where data was generated
previously.

```
$ git-code-debt-generate
```

### Creating your own metrics

1. Create a python project which adds `git-code-debt` as a dependency.
2. Create a package where you'll write your metrics
3. Add your package to `metric_package_names` in your `generate_config.yaml`


The simplest way to write your own custom metrics is to extend
`git_code_debt.metrics.base.SimpleLineCounterBase`.


Here's what the base class looks like

```python

class SimpleLineCounterBase(DiffParserBase):
    # ...

    def should_include_file(self, file_diff_stat: FileDiffStat) -> bool:
        """Implement me to return whether a filename should be included.
        By default, this returns True.

        :param FileDiffStat file_diff_stat:
        """
        return True

    def line_matches_metric(self, line: bytes, file_diff_stat: FileDiffStat) -> bool:
        """Implement me to return whether a line matches the metric.

        :param bytes line: Line in the file
        :param FileDiffStat file_diff_stat:
        """
        raise NotImplementedError
```

Here's an example metric

```python
from git_code_debt.metrics.base import SimpleLineCounterBase


class Python__init__LineCount(SimpleLineCounterBase):
    """Counts the number of lines in __init__.py"""

    def should_include_file(self, file_diff_stat: FileDiffStat) -> bool:
        return file_diff_stat.filename == b'__init__.py'

    def line_matches_metric(self, line: bytes, file_diff_stat -> FileDiffStat) -> bool:
        # All lines in __init__.py match
        return True
```

An additional class is provided which feeds lines as text
(`SimpleLineCounterBase` presents them as `bytes`): `TextLineCounterBase`.
Here is an example metric using that base class:

```python
from git_code_debt.metrics.base import TextLineCounterBase


class XXXLineCount(TextLineCounterBase):
    """Counts the number of lines which are XXX comments"""

    def text_line_matches_metric(self, line: str, file_diff_stat: FileDiffStat) -> bool:
        return '# XXX' in line
```

More complex metrics can extend `DiffParserBase`

```python
class DiffParserBase(object):
    # Specify __metric__ = False to not be included (useful for base classes)
    __metric__ = False

    def get_metrics_from_stat(self, commit: Commit, file_diff_stats: Tuple[FileDiffStat, ...]) -> bool:
        """Implement me to yield Metric objects from the input list of
        FileStat objects.

        Args:
            commit - Commit object
            file_diff_stats - list of FileDiffStat objects

        Returns:
           generator of Metric objects
        """
        raise NotImplementedError

    def get_metrics_info(self) -> List[MetricInfo]:
        """Implement me to yield `MetricInfo` objects."""
        raise NotImplementedError
```


## Some screenshots

### Index
![Example screen index](https://raw.githubusercontent.com/asottile/git-code-debt/master/img/debt_screen_1.png)

### Graph
![Example screen graph](https://raw.githubusercontent.com/asottile/git-code-debt/master/img/debt_screen_2.png)
