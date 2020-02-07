from identify import identify

UNKNOWN = 'unknown'
IGNORED_TAGS = frozenset((
    identify.DIRECTORY, identify.SYMLINK, identify.FILE,
    identify.EXECUTABLE, identify.NON_EXECUTABLE,
    identify.TEXT, identify.BINARY,
))
ALL_TAGS = frozenset((identify.ALL_TAGS - IGNORED_TAGS) | {UNKNOWN})
