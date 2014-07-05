from __future__ import absolute_import
from __future__ import unicode_literals


PYTHON = 'Python'
YAML = 'Yaml'
TEMPLATE = 'Template'
CSS = 'Css'
MAKO_TEMPLATE = 'Mako_Template'
JAVASCRIPT = 'Javascript'
JAVA = 'Java'
ILLUSTRATOR = 'Illustrator'
HTML = 'Html'
CCPP = 'C_C++'
TEXT = 'Text'
SQL = 'SQL'


# Maps a set of file extensions to a nice name.
# Updating this will cause that file type to be tracked for LinesOfCode metric.
FILE_TYPE_MAP = {
    b'.py': PYTHON,

    b'.yaml': YAML,
    b'.yml': YAML,

    b'.css': CSS,
    b'.scss': CSS,

    b'.tmpl': TEMPLATE,

    b'.mako': MAKO_TEMPLATE,

    b'.js': JAVASCRIPT,

    b'.java': JAVA,

    b'.ai': ILLUSTRATOR,

    b'.htm': HTML,
    b'.html': HTML,

    b'.h': CCPP,
    b'.c': CCPP,
    b'.cpp': CCPP,

    b'.md': TEXT,
    b'.rst': TEXT,
    b'.csv': TEXT,
    b'.log': TEXT,
    b'.json': TEXT,
    b'.xml': TEXT,
    b'.txt': TEXT,

    b'.sql': SQL,
}
