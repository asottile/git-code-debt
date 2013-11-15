
PYTHON = 'Python'
YAML = 'Yaml'
TEMPLATE = 'Template'
CSS = 'Css'
MAKO_TEMPLATE = 'Mako_Template'
JAVASCRIPT = 'Javascript'
JAVA = 'Java'
ILLUSTRATOR = 'Illustrator'
HTML = 'Html'
CCPP = 'C/C++'
TEXT = 'Text'
SQL = 'SQL'


# Maps a set of file extensions to a nice name.
# Updating this will cause that file type to be tracked for LinesOfCode metric.
FILE_TYPE_MAP = {
    '.py': PYTHON,

    '.yaml': YAML,
    '.yml': YAML,

    '.css': CSS,
    '.scss': CSS,

    '.tmpl': TEMPLATE,

    '.mako': MAKO_TEMPLATE,

    '.js': JAVASCRIPT,

    '.java': JAVA,

    '.ai': ILLUSTRATOR,

    '.htm': HTML,
    '.html': HTML,

    '.h': CCPP,
    '.c': CCPP,
    '.cpp': CCPP,

    '.md': TEXT,
    '.rst': TEXT,
    '.csv': TEXT,
    '.log': TEXT,
    '.json': TEXT,
    '.xml': TEXT,
    '.txt': TEXT,

    '.sql': SQL,
}
